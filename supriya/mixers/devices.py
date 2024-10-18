from typing import Tuple

from .components import Component


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

    # TODO: set_channel_count(self, channel_count: Optional[ChannelCount] = None) -> None


class Instrument(Device):
    """An instrument device"""

    # TODO: set_channel_count(self, channel_count: Optional[ChannelCount] = None) -> None


class Modulator(Device):
    """A control modulator"""

    pass


class Rack(Device):

    # TODO: set_channel_count(self, channel_count: Optional[ChannelCount] = None) -> None
    # TODO: ungroup()

    async def add_chain(self) -> "Chain":
        return Chain()


class Chain(Component):

    # TODO: add_device() -> Device
    # TODO: add_send(destination: Chain) -> Send
    # TODO: group_devices(index: int, count: int) -> Rack
    # TODO: set_channel_count(self, channel_count: Optional[ChannelCount] = None) -> None

    async def activate(self) -> None:
        pass

    async def deactivate(self) -> None:
        pass

    async def delete(self):
        await self._deallocate()
        self._session = None

    async def move(self, index: int) -> None:
        pass

    async def solo(self) -> None:
        pass

    async def unsolo(self) -> None:
        pass
