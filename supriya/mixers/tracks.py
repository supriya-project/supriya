from typing import List, Optional, Union

from ..contexts import BusGroup, Context, Node
from ..enums import AddAction, CalculationRate
from ..typing import DEFAULT, Default
from .components import AllocatableComponent, C, Component
from .synthdefs import CHANNEL_STRIP_2, PATCH_CABLE_2


class TrackContainer(AllocatableComponent[C]):

    def __init__(self) -> None:
        self._tracks: List[Track] = []

    def _allocate_track(self, track: "Track") -> None:
        # TODO: Annoying that context could be null
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

    async def add_track(self) -> "Track":
        async with self._lock:
            self._tracks.append(track := Track(parent=self))
            if self._can_allocate():
                self._allocate_track(track)
            return track

    @property
    def tracks(self) -> List["Track"]:
        return self._tracks[:]


class Track(TrackContainer[TrackContainer]):

    # TODO: add_device() -> Device
    # TODO: add_send(destination: Track) -> Send
    # TODO: group_devices(index: int, count: int) -> Rack
    # TODO: group_tracks(index: int, count: int) -> Track
    # TODO: set_channel_count(self, channel_count: Optional[ChannelCount] = None) -> None
    # TODO: set_input(None | Default | Track | BusGroup)
    # TODO: set_output(None | Default | Track | BusGroup)

    def __init__(
        self,
        *,
        parent: Optional[TrackContainer] = None,
    ) -> None:
        AllocatableComponent.__init__(self, parent=parent)
        TrackContainer.__init__(self)
        self._output: Optional[Union[Default, Track]] = DEFAULT

    def _allocate(
        self,
        *,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
        context: Context,
        target_bus: BusGroup,
        target_node: Node,
    ) -> None:
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
            if self._output is not None:
                self._nodes["output"] = self._nodes["group"].add_synth(
                    add_action=AddAction.ADD_TO_TAIL,
                    in_=self._audio_buses["main"],
                    out=self._audio_buses["main"],
                    synthdef=PATCH_CABLE_2,
                )
        for track in self.tracks:
            self._allocate_track(track)

    async def activate(self) -> None:
        async with self._lock:
            pass

    async def deactivate(self) -> None:
        async with self._lock:
            pass

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            if self._parent is not None:
                self._parent._delete_track(self)
            self._delete()

    async def move(self, *, index: int, parent: TrackContainer) -> None:
        async with self._lock:
            pass

    async def set_output(self, output: Optional[Union[Default, "Track"]]) -> None:
        async with self._lock:
            pass

    async def solo(self) -> None:
        async with self._lock:
            pass

    async def ungroup(self) -> None:
        async with self._lock:
            pass

    async def unsolo(self) -> None:
        async with self._lock:
            pass

    @property
    def address(self) -> str:
        if self.parent is None:
            return "tracks[?]"
        index = self.parent.tracks.index(self)
        return f"{self.parent.address}.tracks[{index}]"

    @property
    def children(self) -> List[Component]:
        return list(self._tracks)

    @property
    def output(self) -> TrackContainer:
        if isinstance(self._output, Track):
            return self._output
        if self.parent is None:
            raise RuntimeError
        return self.parent
