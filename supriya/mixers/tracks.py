from typing import Generator, List, Optional, Union

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction, CalculationRate
from ..typing import DEFAULT, Default
from .components import AllocatableComponent, C, Component
from .synthdefs import CHANNEL_STRIP_2, PATCH_CABLE_2

"""
Track outputs, like sends and directs, need to be separate from tracks themselves.
During allocation of a subtree, sends may reference a source or target not yet allocated.
Allocation needs to be performed depth-first, with a stack. As we attempt to
allocate each component traversed, the component can flag whether its
allocation must be deferred (throwing it onto the stack). This affords a
two-pass allocation process.

._allocate() and ._deallocate() should be shallow.
Implement ._allocate_deep() and ._deallocate_deep() for traversal.
"""


class TrackContainer(AllocatableComponent[C]):

    def __init__(self) -> None:
        self._tracks: List[Track] = []

    def _delete_track(self, track: "Track") -> None:
        self._tracks.remove(track)

    async def add_track(self) -> "Track":
        async with self._lock:
            self._tracks.append(track := Track(parent=self))
            if context := self._can_allocate():
                track._allocate_deep(context=context)
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

    def __init__(
        self,
        *,
        parent: Optional[TrackContainer] = None,
    ) -> None:
        AllocatableComponent.__init__(self, parent=parent)
        TrackContainer.__init__(self)
        self._output: Optional[Union[Default, TrackContainer]] = DEFAULT
        self._output_bus: Optional[BusGroup] = None  # Cached for reconciliation
        self._setup_output()

    def _allocate(self, *, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        self._audio_buses["main"] = context.add_bus_group(
            calculation_rate=CalculationRate.AUDIO,
            count=2,
        )
        if self.parent is None:
            raise RuntimeError
        target_node = self.parent._nodes["tracks"]
        with context.at():
            self._nodes["group"] = target_node.add_group(
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
            self._reconcile_output()
        return True

    def _output_to_allocatable_component(self) -> Optional[AllocatableComponent]:
        if isinstance(self._output, Default):
            return self._parent
        return self._output

    def _output_to_bus(self) -> Optional[BusGroup]:
        if (output_ := self._output_to_allocatable_component()) is None:
            return output_
        return output_._audio_buses.get("main")

    def _reconcile_output(self) -> None:
        new_output_bus = self._output_to_bus()
        old_output_bus = self._output_bus
        if old_output_bus != new_output_bus:
            if self._nodes.get("output"):
                self._nodes.pop("output").free()
            if new_output_bus is not None:
                self._nodes["output"] = self._nodes["group"].add_synth(
                    add_action=AddAction.ADD_TO_TAIL,
                    in_=self._audio_buses["main"],
                    out=new_output_bus,
                    synthdef=PATCH_CABLE_2,
                )
        self._output_bus = new_output_bus

    def _setup_output(self) -> None:
        if (output := self._output_to_allocatable_component()) is not None:
            output._dependents.add(self)

    def _teardown_output(self) -> None:
        if (
            output := self._output_to_allocatable_component()
        ) is not None and self in output._dependents:
            output._dependents.remove(self)

    def _walk(self) -> Generator[Component, None, None]:
        yield from super()._walk()
        for track in self.tracks:
            yield from track._walk()

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
            # Validate if moving is possible
            if self.mixer is not parent.mixer:
                raise RuntimeError
            elif self in parent.parentage:
                raise RuntimeError
            elif index < 0 or index > len(parent.tracks):
                raise RuntimeError
            # Reconfigure parentage and bail if this is a no-op
            old_parent, old_index = self._parent, 0
            if old_parent is not None:
                old_index = old_parent._tracks.index(self)
            if old_parent is parent and old_index == index:
                return  # Bail
            if old_parent is not None:
                old_parent._tracks.remove(self)
            self._parent = parent
            parent._tracks.insert(index, self)
            # Apply changes against the context
            if (context := self._can_allocate()) is None:
                return  # Bail
            if index == 0:
                node_id = self._parent._nodes["tracks"]
                add_action = AddAction.ADD_TO_HEAD
            else:
                node_id = self._parent._tracks[index - 1]._nodes["group"]
                add_action = AddAction.ADD_AFTER
            with context.at():
                self._nodes["group"].move(target_node=node_id, add_action=add_action)
                self._reconcile_output()

    async def set_output(
        self, output: Optional[Union[Default, TrackContainer]]
    ) -> None:
        async with self._lock:
            if isinstance(output, TrackContainer):
                if output.session is None:
                    output = None
                elif self.mixer is not output.mixer:
                    raise RuntimeError
                elif output is self:
                    raise RuntimeError
                elif output is not None and output is self.parent:
                    output = DEFAULT
            self._teardown_output()
            self._output = output
            self._setup_output()
            if (context := self._can_allocate()) is None:
                return  # Bail
            with context.at():
                self._reconcile_output()

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
    def output(self) -> Optional[Union[Default, TrackContainer]]:
        return self._output
