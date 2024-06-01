import asyncio
from enum import Enum
from typing import Dict, Iterator, List, Literal, Optional, Tuple, TypeAlias, Union

from ..clocks import AsyncClock
from ..contexts import AsyncServer, BusGroup, Context, Node
from ..enums import AddAction
from ..typing import Default

ChannelCount: TypeAlias = Literal[1, 2, 4, 8]


class Component:

    def __init__(self, *, parent: Optional["Component"] = None) -> None:
        self.channel_count: Optional[ChannelCount] = None
        self.context: Optional[Context] = None
        self.is_active: bool = True
        self.nodes: Dict[str, Node] = {}
        self.parent: Optional["Component"] = None

    async def _activate(self) -> None:
        self.is_active = True
        if group := self.nodes.get("group"):
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
        if group := self.nodes.get("group"):
            group.set(active=0)
        self.is_active = False

    async def _deallocate(self) -> None:
        if group := self.nodes.get("group"):
            if not self.is_active:
                group.free()
            else:
                group.set(gate=0)
        self.nodes.clear()

    async def _delete(self) -> None:
        await self._deallocate()
        self.parent = None

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    @property
    def effective_channel_count(self) -> int:
        component = self
        while component.channel_count is None and component.parent is not None:
            component = component.parent
        return component.channel_count or 2


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
        self.channel_count: ChannelCount = 2
        self.clock = AsyncClock()
        self.context_mapping: Dict[AsyncServer, List[Mixer]] = {
            AsyncServer(): [Mixer(session=self)],
        }
        self.status = SessionStatus.OFFLINE
        self.boot_future: Optional[asyncio.Future] = None
        self.quit_future: Optional[asyncio.Future] = None

    async def boot(self) -> None:
        # guard against concurrent boot / quits
        if self.status == SessionStatus.OFFLINE:
            self.quit_future = None
            self.boot_future = asyncio.get_running_loop().create_future()
            self.status = SessionStatus.BOOTING
            await asyncio.gather(*[context.boot() for context in self.context_mapping])
            for context, mixers in self.context_mapping.items():
                for mixer in mixers:
                    with context.at():
                        await mixer._allocate(
                            context=context,
                            target_node=context.default_group,
                        )
            self.status = SessionStatus.ONLINE
            self.boot_future.set_result(True)
        elif self.boot_future is not None:  # BOOTING / ONLINE
            await self.boot_future
        else:  # NONREALTIME
            raise Exception(self.status)

    async def quit(self) -> None:
        # guard against concurrent boot / quits
        if self.status == SessionStatus.ONLINE:
            self.boot_future = None
            self.quit_future = asyncio.get_running_loop().create_future()
            self.status = SessionStatus.QUITTING
            for context, mixers in self.context_mapping.items():
                for mixer in mixers:
                    with context.at():
                        await mixer._deallocate()
            await asyncio.gather(*[context.quit() for context in self.context_mapping])
            self.status = SessionStatus.OFFLINE
            self.quit_future.set_result(True)
        elif self.quit_future is not None:  # QUITTING / OFFLINE
            await self.quit_future
        else:  # NONREALTIME
            raise Exception(self.status)

    async def add_context(self) -> AsyncServer:
        self.context_mapping[context := AsyncServer()] = []
        return context

    async def add_mixer(self, context: Optional[AsyncServer] = None) -> "Mixer":
        if not self.context_mapping:
            context = await self.add_context()
        if context is None:
            context = list(self.context_mapping)[0]
        self.context_mapping.setdefault(context, []).append(
            mixer := Mixer(session=self)
        )
        return mixer

    async def delete_context(self, context: AsyncServer) -> None:
        for mixer in self.context_mapping.pop(context):
            await mixer.delete()


class Mixer(Component):

    def __init__(self, *, session: Optional[Session] = None) -> None:
        super().__init__()
        self.session = session

    async def _allocate(
        self,
        *,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
        channel_count: Optional[ChannelCount] = None,
        context: Context,
        target_node: Node,
    ) -> None:
        self.nodes["group"] = target_node.add_group(add_action=add_action)
        self.nodes["tracks"] = self.nodes["group"].add_group(
            add_action=AddAction.ADD_TO_HEAD
        )
        self.nodes["devices"] = self.nodes["group"].add_group(
            add_action=AddAction.ADD_TO_TAIL
        )

    async def add_device(self) -> "Device":
        return Device()

    async def delete(self):
        await self._deallocate()
        self.session = None

    async def group_devices(self, index: int, count: int) -> "Rack":
        return Rack()

    async def set_channel_count(self, channel_count: ChannelCount) -> None:
        pass

    async def set_context(self, context: Context) -> None:
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
        pass

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
        pass

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
