from typing import TYPE_CHECKING, Generator, List, Optional

from ..contexts import BusGroup, Context, Node
from ..enums import AddAction, CalculationRate
from .components import AllocatableComponent, Component
from .synthdefs import CHANNEL_STRIP_2, PATCH_CABLE_2
from .tracks import Track

if TYPE_CHECKING:
    from .sessions import Session


class Mixer(AllocatableComponent["Session"]):

    # TODO: add_device() -> Device
    # TODO: group_devices(index: int, count: int) -> Rack
    # TODO: set_channel_count(self, channel_count: ChannelCount) -> None
    # TODO: set_output(output: int) -> None

    def __init__(
        self, *, parent: Optional["Session"], session: Optional["Session"] = None
    ) -> None:
        super().__init__(parent=parent, session=session)
        self._tracks: List[Track] = [Track(parent=self, session=self.session)]

    def _allocate(
        self,
        *,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
        context: Context,
        target_bus: BusGroup,
        target_node: Node,
    ) -> None:
        super()._allocate(
            add_action=add_action,
            context=context,
            target_bus=target_bus,
            target_node=target_node,
        )
        self._audio_buses["main"] = context.add_bus_group(
            calculation_rate=CalculationRate.AUDIO,
            count=2,
        )
        with context.at():
            self._nodes["group"] = target_node.add_group(add_action=add_action)
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
                out=target_bus,
                synthdef=PATCH_CABLE_2,
            )
        for track in self.tracks:
            self._allocate_track(track)

    def _allocate_track(self, track: "Track") -> None:
        if self._context is None:
            raise RuntimeError
        track._allocate(
            add_action=AddAction.ADD_TO_TAIL,
            context=self._context,
            target_bus=self._audio_buses["main"],
            target_node=self._nodes["tracks"],
        )

    def _delete_track(self, track: "Track") -> None:
        self._tracks.remove(track)

    def _walk(self) -> Generator[Component, None, None]:
        yield from super()._walk()
        for track in self.tracks:
            yield from track._walk()

    async def add_track(self) -> "Track":
        async with self._lock:
            self._tracks.append(track := Track(parent=self, session=self.session))
            if self._can_allocate():
                self._allocate_track(track)
            return track

    async def delete(self) -> None:
        async with self._lock:
            if self._session is not None:
                self._session._delete_mixer(self)
            self._delete()

    @property
    def address(self) -> str:
        if self.session is None:
            return "mixers[?]"
        index = self.session.mixers.index(self)
        return f"session.mixers[{index}]"

    @property
    def tracks(self) -> list["Track"]:
        return self._tracks[:]
