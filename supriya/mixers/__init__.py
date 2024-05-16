import asyncio
from enum import Enum
from typing import Tuple, Optional, Union, Dict, List

from ..clocks import AsyncClock
from ..contexts import BusGroup, Node, AsyncServer, Context
from ..enums import AddAction
from ..typing import Default


class Component:

    def __init__(self) -> None:
        self.channel_count: Optional[int] = None
        self.context: Optional[Context] = None
        self.is_active: bool = True
        self.nodes: Dict[str, Node] = {}
        self.parent: Optional[Union["Component", "Session"]] = None

    async def _activate(self) -> None:
        self.is_active = True
        if group := self.nodes.get("group"):
            group.unpause()
            group.set(active=1)

    async def _allocate(
        self,
        *,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
        channel_count: Optional[int] = None,
        context: Context,
        target_node: Node,
    ) -> None:
        ...

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

    @property
    def effective_channel_count(self) -> int:
        component = self
        while component.channel_count is None and component.parent is not None:
            component = component.parent
        return component.channel_count or 2


class SessionStatus(Enum):
    OFFLINE = 0
    BOOTING = 1
    REALTIME = 2
    QUITTING = 3


class Session:

    def __init__(self):
        self.channel_count: int = 2
        self.clock = AsyncClock()
        self.context: Optional[AsyncServer] = None
        self.mixer = Mixer()
        self.mixer.parent = self
        self.status = SessionStatus.OFFLINE
        self.boot_future: Optional[asyncio.Future] = None
        self.quit_future: Optional[asyncio.Future] = None

    async def boot(self) -> None:
        # guard against concurrent boot / quits
        if self.status == SessionStatus.OFFLINE:
            self.quit_future = None
            self.boot_future = asyncio.get_running_loop().create_future()
            self.status = SessionStatus.BOOTING
            self.context = await AsyncServer().boot()
            async with self.context.at():
                await self.mixer._allocate(
                    context=self.context,
                    target_node=self.context.default_group,
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
            async with self.context.at():
                await self.mixer._deallocate()
            await self.context.quit()
            self.status = SessionStatus.OFFLINE
            self.context = None
            self.quit_future.set_result(True)
        elif self.quit_future is not None:  # QUITTING / OFFLINE
            await self.quit_future
        else:  # NONREALTIME
            raise Exception(self.status)


class DeviceContainer(Component):
    pass


class TrackContainer(Component):
    pass


"""
Device()
Track(DeviceContainer, TrackContainer[Track])
Mixer(DeviceContainer, TrackContainer[Track])
Chain(DeviceContainer)
Rack(Device, TrackContainer[Chain])
"""


class Mixer(Component):

    def __init__(self):
        super().__init__()
        self.tracks: List[Track] = []

    def _allocate(
        self,
        *,
        context: AsyncServer,
        target_node: Node,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
    ) -> None:
        self.context = context
        self.nodes["group"] = target_node.add_group(add_action=add_action)
        self.nodes["tracks"] = self.nodes["group"].add_group()


class Track(Component):

    async def activate(self) -> None:
        ...

    async def add_device(self) -> "Device":
        ...

    async def add_send(self, destination: "Track") -> "Send":
        ...

    async def add_track(self) -> "Track":
        ...

    async def deactivate(self) -> None:
        ...

    async def delete(self):
        ...

    async def group_devices(self, index: int, count: int) -> "Rack":
        ...

    async def group_tracks(cls, *tracks: "Track") -> "Track":
        ...

    async def move(self, index: Tuple[int, ...]) -> None:
        ...

    async def set_channel_count(self, channel_count: int) -> None:
        ...

    async def set_input(self, input_: Optional[Union[Default, "Track", BusGroup]]) -> None:
        ...

    async def set_output(self, output: Optional[Union[Default, "Track", BusGroup]]) -> None:
        ...

    async def solo(self) -> None:
        ...

    async def ungroup(self) -> None:
        ...

    async def unsolo(self) -> None:
        ...


class Device(Component):

    async def activate(self) -> None:
        ...

    async def deactivate(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    async def move(self, index: Tuple[int, ...]) -> None:
        ...


class AudioDevice(Device):

    async def set_channel_count(self, channel_count: int) -> None:
        ...


class Effect(AudioDevice):
    """An effect device"""
    pass


class Instrument(AudioDevice):
    """An instrument device"""
    pass


class Modulator(Device):
    """A control modulator"""
    pass


class Rack(AudioDevice, Mixer):

    async def ungroup(self) -> None:
        ...


class Connection(Component):
    ...


class Receive(Connection):
    ...


class Direct(Component):
    ...


class DirectIn(Direct):
    ...


class DirectOut(Direct):
    ...


class Send(Connection):

    async def delete(self):
        ...


class Param(Component):
    ...
