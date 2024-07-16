import asyncio
from enum import Enum
from typing import (
    Dict,
    Generic,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
)

from ..clocks import AsyncClock
from ..contexts import AsyncServer, Buffer, Bus, BusGroup, Context, Node
from ..enums import AddAction
from ..osc import find_free_port
from ..typing import Default

ChannelCount: TypeAlias = Literal[1, 2, 4, 8]

C = TypeVar("C", bound="Component")


class Component(Generic[C]):

    def __init__(self, *, parent: Optional["Component"] = None) -> None:
        self._audio_buses: Dict[str, Union[Bus, BusGroup]] = {}
        self._buffers: Dict[str, Buffer] = {}
        self._channel_count: Optional[ChannelCount] = None
        self._context: Optional[Context] = None
        self._control_buses: Dict[str, Union[Bus, BusGroup]] = {}
        self._is_active: bool = True
        self._lock = asyncio.Lock()
        self._nodes: Dict[str, Node] = {}
        self._parent: Optional[C] = None
        self._session: Optional[Session] = None

    async def _activate(self) -> None:
        self._is_active = True
        if group := self._nodes.get("group"):
            group.unpause()
            group.set(active=1)

    async def _allocate(
        self,
        *,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
        channel_count: Optional[ChannelCount] = None,
        context: Context,
        target_node: Node,
    ) -> None:
        pass

    async def _deactivate(self) -> None:
        if group := self._nodes.get("group"):
            group.set(active=0)
        self._is_active = False

    async def _deallocate(self) -> None:
        for key in tuple(self._audio_buses):
            self._audio_buses.pop(key).free()
        for key in tuple(self._control_buses):
            self._control_buses.pop(key).free()
        if group := self._nodes.get("group"):
            if not self._is_active:
                group.free()
            else:
                group.set(gate=0)
        self._nodes.clear()
        for key in tuple(self._buffers):
            self._buffers.pop(key).free()
        self._context = None

    async def _delete(self) -> None:
        await self._deallocate()
        self._parent = None
        self._session = None

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    @property
    def effective_channel_count(self) -> int:
        channel_count = 2
        for component in self._iterate_parentage():
            if component._channel_count:
                return component._channel_count
        return channel_count

    @property
    def parent(self) -> Optional[C]:
        return self._parent


class SessionStatus(Enum):
    OFFLINE = 0
    BOOTING = 1
    ONLINE = 2
    QUITTING = 3


class Session:
    """
    Top-level object.

    Contains one transport.

    Contains one or more contexts.

    Contains one or more mixers.

    Each mixer references one context.

    This supports running scsynth and supernova simultaneously via two mixers.
    """

    def __init__(self) -> None:
        self._boot_future: Optional[asyncio.Future] = None
        self._channel_count: ChannelCount = 2
        self._clock = AsyncClock()
        self._contexts: Dict[AsyncServer, List[Mixer]] = {
            (context := AsyncServer()): [mixer := Mixer(session=self)],
        }
        self._lock = asyncio.Lock()
        self._mixers: Dict[Mixer, AsyncServer] = {mixer: context}
        self._quit_future: Optional[asyncio.Future] = None
        self._status = SessionStatus.OFFLINE

    async def add_context(self) -> AsyncServer:
        async with self._lock:
            self._contexts[context := AsyncServer()] = []
            if self._status == SessionStatus.ONLINE:
                await context.boot(port=find_free_port())
            return context

    def _delete_mixer(self, mixer) -> None:
        self._contexts[self._mixers.pop(mixer)].remove(mixer)

    async def add_mixer(self, context: Optional[AsyncServer] = None) -> "Mixer":
        async with self._lock:
            if not self._contexts:
                context = await self.add_context()
            if context is None:
                context = list(self._contexts)[0]
            self._contexts.setdefault(context, []).append(mixer := Mixer(session=self))
            self._mixers[mixer] = context
            if self._status == SessionStatus.ONLINE:
                await mixer._allocate(
                    context=context,
                    target_node=context.default_group,
                )
            return mixer

    async def boot(self) -> None:
        async with self._lock:
            # guard against concurrent boot / quits
            if self._status == SessionStatus.OFFLINE:
                self._quit_future = None
                self._boot_future = asyncio.get_running_loop().create_future()
                self._status = SessionStatus.BOOTING
                await asyncio.gather(
                    *[context.boot(port=find_free_port()) for context in self._contexts]
                )
                self._status = SessionStatus.ONLINE
                self._boot_future.set_result(True)
                for context, mixers in self._contexts.items():
                    for mixer in mixers:
                        with context.at():
                            await mixer._allocate(
                                context=context,
                                target_node=context.default_group,
                            )
            elif self._boot_future is not None:  # BOOTING / ONLINE
                await self._boot_future
            else:  # NONREALTIME
                raise Exception(self._status)

    async def delete_context(self, context: AsyncServer) -> None:
        async with self._lock:
            for mixer in self._contexts.pop(context):
                await mixer.delete()
            await context.quit()

    async def quit(self) -> None:
        async with self._lock:
            # guard against concurrent boot / quits
            if self._status == SessionStatus.ONLINE:
                self._boot_future = None
                self._quit_future = asyncio.get_running_loop().create_future()
                self._status = SessionStatus.QUITTING
                for context, mixers in self._contexts.items():
                    for mixer in mixers:
                        with context.at():
                            await mixer._deallocate()
                await asyncio.gather(*[context.quit() for context in self._contexts])
                self._status = SessionStatus.OFFLINE
                self._quit_future.set_result(True)
            elif self._quit_future is not None:  # QUITTING / OFFLINE
                await self._quit_future
            elif self._status == SessionStatus.OFFLINE:  # Never booted
                return
            else:  # NONREALTIME
                raise Exception(self._status)

    async def set_mixer_context(self, mixer: "Mixer", context: AsyncServer) -> None:
        if mixer not in self._mixers:
            raise ValueError(mixer)
        elif context not in self._contexts:
            raise ValueError(context)
        if context is mixer._context:
            return
        async with self._lock:
            self._contexts[self._mixers[mixer]].remove(mixer)
            async with mixer._lock:
                await mixer._deallocate()
                if self._status == SessionStatus.ONLINE:
                    await mixer._allocate(
                        context=context, target_node=context.default_group
                    )
                self._contexts[context].append(mixer)
                self._mixers[mixer] = context

    @property
    def contexts(self):
        return list(self._contexts)

    @property
    def mixers(self):
        return list(self._mixers)


class Mixer(Component):

    def __init__(self, *, session: Optional[Session] = None) -> None:
        super().__init__()
        self._session = session

    async def _allocate(
        self,
        *,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
        channel_count: Optional[ChannelCount] = None,
        context: Context,
        target_node: Node,
    ) -> None:
        self._nodes["group"] = target_node.add_group(add_action=add_action)
        self._nodes["tracks"] = self._nodes["group"].add_group(
            add_action=AddAction.ADD_TO_HEAD
        )
        self._nodes["devices"] = self._nodes["group"].add_group(
            add_action=AddAction.ADD_TO_TAIL
        )

    async def add_device(self) -> "Device":
        return Device()

    async def add_track(self) -> "Track":
        return Track()

    async def delete(self):
        if self._session is not None:
            self._session._delete_mixer(self)
        await self._delete()

    async def group_devices(self, index: int, count: int) -> "Rack":
        return Rack()

    async def set_channel_count(self, channel_count: ChannelCount) -> None:
        pass

    async def set_output(self, output: BusGroup) -> None:
        pass


class Track(Component):

    async def activate(self) -> None:
        pass

    async def add_device(self) -> "Device":
        return Device()

    async def add_send(self, destination: "Track") -> "Send":
        return Send()

    async def add_track(self) -> "Track":
        return Track()

    async def deactivate(self) -> None:
        pass

    async def delete(self):
        await self._deallocate()
        self._session = None

    async def group_devices(self, index: int, count: int) -> "Rack":
        return Rack()

    async def group_tracks(cls, *tracks: "Track") -> "Track":
        return Track()

    async def move(self, index: Tuple[int, ...]) -> None:
        pass

    async def set_channel_count(self, channel_count: Optional[ChannelCount]) -> None:
        pass

    async def set_input(
        self, input_: Optional[Union[Default, "Track", BusGroup]]
    ) -> None:
        pass

    async def set_output(
        self, output: Optional[Union[Default, "Track", BusGroup]]
    ) -> None:
        pass

    async def solo(self) -> None:
        pass

    async def ungroup(self) -> None:
        pass

    async def unsolo(self) -> None:
        pass


class Chain(Component):

    async def activate(self) -> None:
        pass

    async def add_device(self) -> "Device":
        return Device()

    async def add_send(self, destination: "Chain") -> "Send":
        return Send()

    async def deactivate(self) -> None:
        pass

    async def delete(self):
        await self._deallocate()
        self._session = None

    async def group_devices(self, index: int, count: int) -> "Rack":
        return Rack()

    async def move(self, index: Tuple[int, ...]) -> None:
        pass

    async def set_channel_count(
        self, channel_count: Optional[ChannelCount] = None
    ) -> None:
        pass

    async def solo(self) -> None:
        pass

    async def unsolo(self) -> None:
        pass


class Device(Component):

    async def activate(self) -> None:
        pass

    async def deactivate(self) -> None:
        pass

    async def delete(self) -> None:
        pass

    async def move(self, index: Tuple[int, ...]) -> None:
        pass


class Effect(Device):
    """An effect device"""

    async def set_channel_count(
        self, channel_count: Optional[ChannelCount] = None
    ) -> None:
        pass


class Instrument(Device):
    """An instrument device"""

    async def set_channel_count(
        self, channel_count: Optional[ChannelCount] = None
    ) -> None:
        pass


class Modulator(Device):
    """A control modulator"""

    pass


class Rack(Device):

    async def add_chain(self) -> Chain:
        return Chain()

    async def set_channel_count(
        self, channel_count: Optional[ChannelCount] = None
    ) -> None:
        pass

    async def ungroup(self) -> None:
        pass


class Connection(Component):
    pass


class Receive(Connection):
    pass


class Direct(Component):
    pass


class DirectIn(Direct):
    pass


class DirectOut(Direct):
    pass


class Send(Connection):

    async def delete(self):
        pass


class Param(Component):
    pass
