from typing import List, Optional, Union, cast

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction, CalculationRate
from ..typing import DEFAULT, Default
from .components import AllocatableComponent, C, Component
from .routing import Connectable, Connection
from .synthdefs import CHANNEL_STRIP_2, PATCH_CABLE_2


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


class TrackOutput(Connection["Track"]):

    def __init__(
        self,
        *,
        parent: "Track",
        target: Connectable = DEFAULT,
    ) -> None:
        super().__init__(
            name="output",
            parent=parent,
            source=parent,
            target=target,
        )

    def _resolve_default_source_component(self) -> Optional[AllocatableComponent]:
        return self.parent

    def _resolve_default_target_component(self) -> Optional[AllocatableComponent]:
        return self.parent and self.parent.parent

    async def set_target(self, target: Connectable) -> None:
        async with self._lock:
            if target is self.parent:
                raise RuntimeError
            self._set_target(target)


class TrackSend(Connection["Track"]):
    def __init__(
        self,
        *,
        parent: "Track",
        target: Union[AllocatableComponent, BusGroup],
        postfader: bool = True,
    ) -> None:
        super().__init__(
            name="send",
            parent=parent,
            source=parent,
            target=target,
        )
        self._postfader = postfader
        self._cached_postfader = postfader

    def _allocate_synth(
        self, parent: AllocatableComponent, source_bus: BusGroup, target_bus: BusGroup
    ) -> None:
        self._nodes["synth"] = parent._nodes["channel_strip"].add_synth(
            add_action=AddAction.ADD_AFTER if self._postfader else AddAction.ADD_BEFORE,
            in_=source_bus,
            out=target_bus,
            synthdef=PATCH_CABLE_2,
        )

    def _cache(
        self, new_source_bus: Optional[BusGroup], new_target_bus: Optional[BusGroup]
    ) -> None:
        super()._cache(new_source_bus, new_target_bus)
        self._cached_postfader = self._postfader

    def _resolve_default_source_component(self) -> Optional[AllocatableComponent]:
        return self.parent

    def _should_reallocate(
        self, new_source_bus: Optional[BusGroup], new_target_bus: Optional[BusGroup]
    ) -> bool:
        return super()._should_reallocate(new_source_bus, new_target_bus) or (
            self._postfader != self._cached_postfader
        )

    async def delete(self) -> None:
        async with self._lock:
            if self._parent is not None and self in self._parent._sends:
                self._parent._sends.remove(self)
            self._delete()

    async def set_postfader(self, postfader: bool) -> None:
        async with self._lock:
            self._postfader = postfader
            if (context := self._can_allocate()) is not None:
                with context.at():
                    self._reconcile_server_side()

    async def set_target(self, target: Union[AllocatableComponent, BusGroup]) -> None:
        async with self._lock:
            if target is self.parent:
                raise RuntimeError
            self._set_target(target)

    @property
    def postfader(self) -> bool:
        return self._postfader

    @property
    def target(self) -> Union[AllocatableComponent, BusGroup]:
        # TODO: Can this be parameterized via generics?
        return cast(Union[AllocatableComponent, BusGroup], self._target)


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
        self._output = TrackOutput(parent=self)
        # TODO: Are sends the purview of track containers in general?
        self._sends: List[TrackSend] = []

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
        return True

    async def activate(self) -> None:
        async with self._lock:
            pass

    async def add_send(
        self, *, postfader: bool, target: Union[AllocatableComponent, BusGroup]
    ) -> TrackSend:
        async with self._lock:
            self._sends.append(
                send := TrackSend(parent=self, postfader=postfader, target=target)
            )
            if context := self._can_allocate():
                send._allocate_deep(context=context)
            return send

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
                for component in self._dependents:
                    component._reconcile()

    async def set_output(
        self, output: Optional[Union[Default, TrackContainer]]
    ) -> None:
        await self._output.set_target(output)

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
        prefader_sends = []
        postfader_sends = []
        for send in self._sends:
            if send.postfader:
                postfader_sends.append(send)
            else:
                prefader_sends.append(send)
        return [*self._tracks, *prefader_sends, self._output, *postfader_sends]

    @property
    def output(self) -> Connectable:
        return self._output._target

    @property
    def sends(self) -> List[TrackSend]:
        return self._sends[:]
