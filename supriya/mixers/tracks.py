import dataclasses
from typing import Union, cast

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction
from ..typing import DEFAULT, Default
from ..ugens import SynthDef
from .components import C, ChannelCount, Component, ComponentNames, H, State
from .devices import DeviceContainer
from .routing import Connection, ConnectionState
from .synthdefs import (
    build_channel_strip,
    build_meters,
    build_patch_cable,
)


class TrackContainer(Component[C, H]):

    def __init__(self) -> None:
        self._tracks: list[Track] = []

    def _add_track(self, name: str | None = None) -> "Track":
        self._tracks.append(track := Track(name=name, parent=self))
        return track

    def _group(self, index: int, count: int) -> "Track":
        if index < 0:
            raise ValueError(index)
        elif count < 1:
            raise ValueError(count)
        elif (index + count) > len(self.tracks):
            raise ValueError(index, count)
        child_tracks = self._tracks[index : index + count]
        group_track = Track(parent=self)
        self._tracks.insert(index, group_track)
        for i, child_track in enumerate(child_tracks):
            child_track._move(parent=group_track, index=i)
        return group_track

    async def add_track(self, name: str | None = None) -> "Track":
        async with self._lock:
            track = self._add_track(name=name)
            if context := self._can_allocate():
                await track._allocate_deep(context=context)
            return track

    async def group(self, index: int, count: int) -> "Track":
        async with self._lock:
            return self._group(index=index, count=count)

    @property
    def tracks(self) -> list["Track"]:
        return self._tracks[:]


class TrackFeedback(Connection["Track", BusGroup, "Track"]):
    def __init__(
        self,
        *,
        parent: "Track",
        source: BusGroup | None = None,
    ) -> None:
        super().__init__(
            kind="feedback",
            parent=parent,
            source=source,
            target=parent,
        )

    def _allocate_synth(
        self,
        *,
        context: AsyncServer,
        parent: Component,
        new_state: ConnectionState,
    ) -> None:
        self._nodes[ComponentNames.SYNTH] = parent._nodes[
            ComponentNames.GROUP
        ].add_synth(
            active=parent._control_buses[ComponentNames.ACTIVE].map_symbol(),
            add_action=AddAction.ADD_TO_HEAD,
            in_=new_state.source_bus,
            out=new_state.target_bus,
            synthdef=build_patch_cable(2, 2, feedback=True),
        )


class TrackInput(Connection["Track", Union[BusGroup, "Track"], "Track"]):

    def __init__(
        self,
        *,
        parent: "Track",
        source: Union[BusGroup, "Track"] | None = None,
    ) -> None:
        super().__init__(
            kind="input",
            parent=parent,
            source=source,
            target=parent,
            writing=False,
        )

    def __repr__(self) -> str:
        source: str = "null"
        if isinstance(self._source, Track):
            source = self._source.address
        elif isinstance(self._source, BusGroup):
            source = self._source.map_symbol()
        return f"<{type(self).__name__} {self.address} source={source}>"

    def _allocate_synth(
        self,
        *,
        context: AsyncServer,
        parent: Component,
        new_state: ConnectionState,
    ) -> None:
        self._nodes[ComponentNames.SYNTH] = parent._nodes[
            ComponentNames.TRACKS
        ].add_synth(
            active=parent._control_buses[ComponentNames.ACTIVE].map_symbol(),
            add_action=AddAction.ADD_BEFORE,
            in_=new_state.source_bus,
            out=new_state.target_bus,
            synthdef=build_patch_cable(2, 2, feedback=bool(new_state.feedsback)),
        )

    def _disconnect_dependency(
        self, root: "Component", dependency: "Component"
    ) -> None:
        if root in tuple(self._iterate_parentage()):
            return
        if dependency is self._source:
            self._set_source(None)

    def _set_source(self, source: Union[BusGroup, "Track"] | None) -> None:
        if source is self.parent:
            raise RuntimeError
        super()._set_source(source)

    async def set_source(self, source: Union[BusGroup, "Track"] | None) -> None:
        async with self._lock:
            self._set_source(source)


class TrackOutput(Connection["Track", "Track", BusGroup | Default | TrackContainer]):

    def __init__(
        self,
        *,
        parent: "Track",
        target: BusGroup | Default | TrackContainer | None = DEFAULT,
    ) -> None:
        super().__init__(
            kind="output",
            parent=parent,
            source=parent,
            target=target,
        )

    def __repr__(self) -> str:
        target: str = "null"
        if isinstance(self._target, TrackContainer):
            target = self._target.address
        elif isinstance(self._target, BusGroup):
            target = self._target.map_symbol()
        elif isinstance(self._target, Default):
            target = "default"
        return f"<{type(self).__name__} {self.address} target={target}>"

    def _resolve_default_target(
        self, context: AsyncServer | None
    ) -> tuple[Component | None, BusGroup | None]:
        return (self.parent and self.parent.parent), None

    def _disconnect_dependency(
        self, root: "Component", dependency: "Component"
    ) -> None:
        if root in tuple(self._iterate_parentage()):
            return
        if dependency is self._target:
            self._set_target(None)

    def _set_target(self, target: BusGroup | Default | TrackContainer | None) -> None:
        if target is self.parent:
            raise RuntimeError
        super()._set_target(target)

    async def set_target(
        self, target: BusGroup | Default | TrackContainer | None
    ) -> None:
        async with self._lock:
            self._set_target(target)


class TrackSend(Connection["Track", "Track", TrackContainer]):
    def __init__(
        self,
        *,
        parent: "Track",
        target: TrackContainer,
        postfader: bool = True,
    ) -> None:
        super().__init__(
            kind="send",
            parent=parent,
            postfader=postfader,
            source=parent,
            target=target,
        )

    def __repr__(self) -> str:
        target: str = "null"
        if isinstance(self._target, TrackContainer):
            target = self._target.address
        return f"<{type(self).__name__} {self.address} target={target}>"

    def _allocate_synth(
        self,
        *,
        context: AsyncServer,
        parent: Component,
        new_state: ConnectionState,
    ) -> None:
        self._nodes[ComponentNames.SYNTH] = parent._nodes[
            ComponentNames.CHANNEL_STRIP
        ].add_synth(
            active=parent._control_buses[ComponentNames.ACTIVE].map_symbol(),
            add_action=(
                AddAction.ADD_AFTER if new_state.postfader else AddAction.ADD_BEFORE
            ),
            in_=new_state.source_bus,
            out=new_state.target_bus,
            synthdef=build_patch_cable(2, 2),
        )

    def _disconnect_dependency(
        self, root: "Component", dependency: "Component"
    ) -> None:
        if root in tuple(self._iterate_parentage()):
            return
        self._delete()

    def _disconnect_parentage(self) -> None:
        if self._parent is not None and self in self._parent._sends:
            self._parent._sends.remove(self)
        super()._disconnect_parentage()

    def _resolve_default_source(
        self, context: AsyncServer | None
    ) -> tuple[Component | None, BusGroup | None]:
        return self.parent, None

    def _set_target(self, target: TrackContainer | None) -> None:
        if target is self.parent:
            raise RuntimeError
        super()._set_target(target)

    async def delete(self) -> None:
        async with self._lock:
            self._delete()

    async def set_inverted(self, inverted: bool) -> None:
        async with self._lock:
            self._set_inverted(inverted)

    async def set_postfader(self, postfader: bool) -> None:
        async with self._lock:
            self._set_postfader(postfader)

    async def set_target(self, target: TrackContainer) -> None:
        async with self._lock:
            self._set_target(target)

    @property
    def address(self) -> str:
        if self.parent is None:
            return "sends[?]"
        index = self.parent.sends.index(self)
        return f"{self.parent.address}.sends[{index}]"

    @property
    def inverted(self) -> bool:
        return self._inverted

    @property
    def postfader(self) -> bool:
        return self._postfader

    @property
    def target(self) -> Component | BusGroup:
        # TODO: Can this be parameterized via generics?
        return cast(Component | BusGroup, self._target)


@dataclasses.dataclass
class TrackState(State):
    channel_count: ChannelCount = 2


class Track(
    TrackContainer[TrackContainer, TrackState],
    DeviceContainer[TrackContainer, TrackState],
):

    # TODO: add_device() -> Device
    # TODO: group_devices(index: int, count: int) -> Rack
    # TODO: group_tracks(index: int, count: int) -> Track
    # TODO: set_channel_count(self, channel_count: ChannelCount | None = None) -> None

    def __init__(
        self,
        *,
        name: str | None = None,
        parent: TrackContainer | None = None,
    ) -> None:
        Component.__init__(self, name=name, parent=parent)
        DeviceContainer.__init__(self)
        TrackContainer.__init__(self)
        self._feedback = TrackFeedback(parent=self)
        self._input = TrackInput(parent=self)
        self._is_muted: bool = False
        self._is_soloed: bool = False
        self._output = TrackOutput(parent=self)
        # TODO: Are sends the purview of track containers in general?
        self._sends: list[TrackSend] = []

    def _add_send(
        self, target: TrackContainer, postfader: bool = True, inverted: bool = False
    ) -> TrackSend:
        if self.mixer is not target.mixer:
            raise RuntimeError
        self._sends.append(
            send := TrackSend(parent=self, postfader=postfader, target=target)
        )
        return send

    def _allocate(self, *, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        elif self.parent is None:
            raise RuntimeError
        main_audio_bus = self._get_audio_bus(
            context, name=ComponentNames.MAIN, can_allocate=True
        )
        active_control_bus = self._get_control_bus(
            context, name=ComponentNames.ACTIVE, can_allocate=True
        )
        gain_control_bus = self._get_control_bus(
            context, name=ComponentNames.GAIN, can_allocate=True
        )
        input_levels_control_bus = self._get_control_bus(
            context,
            name=ComponentNames.INPUT_LEVELS,
            can_allocate=True,
            channel_count=2,
        )
        output_levels_control_bus = self._get_control_bus(
            context,
            name=ComponentNames.OUTPUT_LEVELS,
            can_allocate=True,
            channel_count=2,
        )
        target_node = self.parent._nodes[ComponentNames.TRACKS]
        with context.at():
            self._update_activation(True)
            gain_control_bus.set(0.0)
            input_levels_control_bus.set(0.0)
            output_levels_control_bus.set(0.0)
            self._nodes[ComponentNames.GROUP] = group = target_node.add_group(
                add_action=AddAction.ADD_TO_TAIL
            )
            self._nodes[ComponentNames.TRACKS] = tracks = group.add_group(
                add_action=AddAction.ADD_TO_HEAD
            )
            self._nodes[ComponentNames.DEVICES] = group.add_group(
                add_action=AddAction.ADD_TO_TAIL
            )
            self._nodes[ComponentNames.CHANNEL_STRIP] = channel_strip = group.add_synth(
                add_action=AddAction.ADD_TO_TAIL,
                bus=main_audio_bus,
                active=active_control_bus.map_symbol(),
                gain=gain_control_bus.map_symbol(),
                synthdef=build_channel_strip(2),
            )
            self._nodes[ComponentNames.INPUT_LEVELS] = tracks.add_synth(
                add_action=AddAction.ADD_AFTER,
                synthdef=build_meters(2),
                in_=self._audio_buses[ComponentNames.MAIN],
                out=input_levels_control_bus,
            )
            self._nodes[ComponentNames.OUTPUT_LEVELS] = channel_strip.add_synth(
                add_action=AddAction.ADD_AFTER,
                synthdef=build_meters(2),
                in_=self._audio_buses[ComponentNames.MAIN],
                out=output_levels_control_bus,
            )
        return True

    def _disconnect_parentage(self) -> None:
        if self._parent is not None:
            self._parent._tracks.remove(self)
        super()._disconnect_parentage()

    def _get_synthdefs(self) -> list[SynthDef]:
        return [
            build_channel_strip(2),
            build_meters(2),
        ]

    def _move(self, parent: TrackContainer, index: int) -> None:
        # Validate if moving is possible
        if self.mixer is not parent.mixer:
            raise RuntimeError
        elif self in parent.parentage:
            raise RuntimeError
        elif index < 0:
            raise RuntimeError
        elif index and index >= len(parent.tracks):
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
        if (context := self._can_allocate()) is not None:
            if index == 0:
                node_id = self._parent._nodes[ComponentNames.TRACKS]
                add_action = AddAction.ADD_TO_HEAD
            else:
                node_id = self._parent._tracks[index - 1]._nodes[ComponentNames.GROUP]
                add_action = AddAction.ADD_AFTER
            with context.at():
                self._nodes[ComponentNames.GROUP].move(
                    target_node=node_id, add_action=add_action
                )
        for component in sorted(self._dependents, key=lambda x: x.graph_order):
            component._reconcile(context)

    def _register_feedback(
        self, context: AsyncServer | None, dependent: "Component"
    ) -> BusGroup | None:
        super()._register_feedback(context, dependent)
        # check if feedback should be setup
        if not context:
            return None
        if self._feedback_dependents:
            self._feedback._set_source(
                self._get_audio_bus(
                    context, name=ComponentNames.FEEDBACK, can_allocate=True
                )
            )
        return self._get_audio_bus(context, name=ComponentNames.FEEDBACK)

    def _set_muted(self, muted: bool = True) -> None:
        self._is_muted = muted
        self._update_activation()

    def _set_soloed(self, soloed: bool = True, exclusive: bool = True) -> None:
        self._is_soloed = soloed
        if not (mixer := self.mixer):
            return
        if soloed:
            if exclusive:
                mixer._soloed_tracks.discard(self)
                for track in mixer._soloed_tracks:
                    track._is_soloed = False
            mixer._soloed_tracks.add(self)
        else:
            mixer._soloed_tracks.discard(self)
        for component in mixer._walk(Track):
            if isinstance(component, Track):
                component._update_activation()

    def _ungroup(self) -> None:
        if not (parent := self.parent):
            raise ValueError
        group_track_index = parent.tracks.index(self)
        for i, track in enumerate(self._tracks[:], 1):
            track._move(parent=self.parent, index=group_track_index + i)
        self._delete()

    def _unregister_feedback(self, dependent: "Component") -> bool:
        if should_tear_down := super()._unregister_feedback(dependent):
            # check if feedback should be torn down
            if bus_group := self._audio_buses.get(ComponentNames.FEEDBACK):
                bus_group.free()
            self._feedback._set_source(None)
        return should_tear_down

    def _update_activation(self, force=True) -> None:
        if not (mixer := self.mixer):
            return
        was_active = self._is_active
        self._is_active = not self._is_muted
        if mixer._soloed_tracks:
            self._is_active = self._is_active and any(
                track._is_soloed
                for track in self._iterate_parentage()
                if isinstance(track, Track)
            )
        if self._can_allocate() and (force or (was_active != self._is_active)):
            self._control_buses[ComponentNames.ACTIVE].set(float(self._is_active))

    async def add_send(
        self, target: TrackContainer, postfader: bool = True, inverted: bool = False
    ) -> TrackSend:
        async with self._lock:
            send = self._add_send(target=target, postfader=postfader, inverted=inverted)
            if context := self._can_allocate():
                await send._allocate_deep(context=context)
            return send

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            self._delete()

    async def move(self, parent: TrackContainer, index: int) -> None:
        async with self._lock:
            self._move(parent=parent, index=index)

    async def set_input(self, input_: Union[BusGroup, "Track"] | None) -> None:
        await self._input.set_source(input_)

    async def set_muted(self, muted: bool = True) -> None:
        async with self._lock:
            self._set_muted(muted)

    def set_name(self, name: str | None = None) -> None:
        self._name = name

    async def set_output(
        self, output: BusGroup | Default | TrackContainer | None
    ) -> None:
        await self._output.set_target(output)

    async def set_soloed(self, soloed: bool = True, exclusive: bool = True) -> None:
        async with self._lock:
            self._set_soloed(soloed=soloed, exclusive=exclusive)

    async def ungroup(self) -> None:
        async with self._lock:
            self._ungroup()

    @property
    def address(self) -> str:
        if self.parent is None:
            return "tracks[?]"
        index = self.parent.tracks.index(self)
        return f"{self.parent.address}.tracks[{index}]"

    @property
    def children(self) -> list[Component]:
        prefader_sends = []
        postfader_sends = []
        for send in self._sends:
            if send.postfader:
                postfader_sends.append(send)
            else:
                prefader_sends.append(send)
        return [
            self._feedback,
            self._input,
            *self._tracks,
            *self._devices,
            *prefader_sends,
            self._output,
            *postfader_sends,
        ]

    @property
    def input_(self) -> BusGroup | TrackContainer | None:
        return self._input._source

    @property
    def input_levels(self) -> tuple[float, ...]:
        if (
            (bus := self._control_buses.get(ComponentNames.INPUT_LEVELS))
            and (context := self._can_allocate())
            and context.shared_memory
        ):
            return context.shared_memory[bus.id_ : bus.id_ + len(bus)]
        return (0.0,) * 2

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def output(self) -> BusGroup | Default | TrackContainer | None:
        return self._output._target

    @property
    def output_levels(self) -> tuple[float, ...]:
        if (
            (bus := self._control_buses.get(ComponentNames.OUTPUT_LEVELS))
            and (context := self._can_allocate())
            and context.shared_memory
        ):
            return context.shared_memory[bus.id_ : bus.id_ + len(bus)]
        # TODO: Implement SHM on Windows
        return (0.0,) * 2

    @property
    def sends(self) -> list[TrackSend]:
        return self._sends[:]
