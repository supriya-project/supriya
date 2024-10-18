from typing import TYPE_CHECKING, List, Optional

from ..contexts import AsyncServer
from ..enums import AddAction, CalculationRate
from .components import AllocatableComponent, Component
from .synthdefs import CHANNEL_STRIP_2, PATCH_CABLE_2
from .tracks import Track, TrackContainer

if TYPE_CHECKING:
    from .sessions import Session


class Mixer(TrackContainer["Session"]):

    # TODO: add_device() -> Device
    # TODO: group_devices(index: int, count: int) -> Rack
    # TODO: set_channel_count(self, channel_count: ChannelCount) -> None
    # TODO: set_output(output: int) -> None

    def __init__(self, *, parent: Optional["Session"]) -> None:
        AllocatableComponent.__init__(self, parent=parent)
        TrackContainer.__init__(self)
        self._tracks.append(Track(parent=self))

    def _allocate(self, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        self._audio_buses["main"] = context.add_bus_group(
            calculation_rate=CalculationRate.AUDIO,
            count=2,
        )
        with context.at():
            self._nodes["group"] = context.default_group.add_group(
                add_action=AddAction.ADD_TO_TAIL
            )
            self._nodes["tracks"] = self._nodes["group"].add_group(
                add_action=AddAction.ADD_TO_HEAD
            )
            self._nodes["channel_strip"] = self._nodes["group"].add_synth(
                add_action=AddAction.ADD_TO_TAIL,
                bus=self._audio_buses["main"],
                synthdef=CHANNEL_STRIP_2,
            )
            self._nodes["output"] = self._nodes["group"].add_synth(
                add_action=AddAction.ADD_TO_TAIL,
                in_=self._audio_buses["main"],
                out=context.audio_output_bus_group,
                synthdef=PATCH_CABLE_2,
            )
        return True

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            if self.session is not None:
                self.session._delete_mixer(self)
            self._delete()

    @property
    def address(self) -> str:
        if self.session is None:
            return "mixers[?]"
        index = self.session.mixers.index(self)
        return f"session.mixers[{index}]"

    @property
    def children(self) -> List[Component]:
        return [*self._tracks]

    @property
    def context(self) -> Optional[AsyncServer]:
        if self.parent is None:
            return None
        return self.parent._mixers[self]
