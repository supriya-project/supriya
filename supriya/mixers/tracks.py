from typing import Optional, Union

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction, CalculationRate, DoneAction
from ..typing import DEFAULT, Default
from .components import (
    C,
    Component,
)
from .constants import IO, Address, Names
from .devices import DeviceContainer
from .specs import (
    BusSpec,
    GroupSpec,
    Spec,
    SynthDefSpec,
    SynthSpec,
)
from .synthdefs import build_channel_strip, build_meters, build_patch_cable


class TrackContainer(Component[C]):
    def __init__(self) -> None:
        self._tracks: list[Track] = []

    def _add_track(self, name: str | None = None) -> "Track":
        if (session := self.session) is None:
            raise RuntimeError
        self._tracks.append(
            track := Track(id_=session._get_next_id(), name=name, parent=self)
        )
        return track

    def _group(self, index: int, count: int) -> "Track":
        if (session := self.session) is None:
            raise RuntimeError
        if index < 0:
            raise ValueError(index)
        elif count < 1:
            raise ValueError(count)
        elif (index + count) > len(self.tracks):
            raise ValueError(index, count)
        child_tracks = self._tracks[index : index + count]
        group_track = Track(id_=session._get_next_id(), parent=self)
        self._tracks.insert(index, group_track)
        for i, child_track in enumerate(child_tracks):
            child_track._move(parent=group_track, index=i)
        return group_track

    async def add_track(self, name: str | None = None) -> "Track":
        async with self._lock:
            track = self._add_track(name=name)
            if context := self._can_allocate():
                await track._reconcile(context=context)
            else:
                track._reconcile_connections()
            return track

    async def group(self, index: int, count: int) -> "Track":
        async with self._lock:
            track = self._group(index=index, count=count)
            if context := self._can_allocate():
                await track._reconcile(context=context)
            else:
                track._reconcile_connections()
            return track

    @property
    def tracks(self) -> list["Track"]:
        return self._tracks[:]


class TrackSend(Component["Track"]):
    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: Optional["Track"] = None,
        postfader: bool = True,
        target: TrackContainer,
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)
        self._postfader = postfader
        self._target = target

    def __repr__(self) -> str:
        return (
            super()
            .__repr__()
            .replace(
                ">",
                f" {'postfader' if self.postfader else 'prefader'}"
                f" target={Component.__repr__(self.target)}>",
            )
        )

    def _disconnect_parentage(self) -> None:
        if (parent := self._parent) is not None and self in parent._sends:
            parent._sends.remove(self)
        super()._disconnect_parentage()

    def _notify_disconnected(self, connection: "Component") -> bool:
        return connection is self._target

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        root: Component | None = None,
    ) -> tuple[list[Component], set[Component]]:
        if self.parent is None:
            raise ValueError
        related, deleted = super()._reconcile_connections(deleting=deleting, root=root)
        components: list[Component] = [self.parent, self.target]
        if deleting:
            self.parent._connections.pop((self, Names.INPUT), None)
            self.target._connections.pop((self, Names.OUTPUT), None)
        else:
            self.parent._connections[(self, Names.INPUT)] = IO.READ
            self.target._connections[(self, Names.OUTPUT)] = IO.WRITE
        related.extend(sorted(components, key=lambda x: x.graph_order))
        return related, deleted

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not self.parent:
            raise RuntimeError
        if not context:
            return []
        feedsback = bool(
            Spec.feedsback(
                writer_order=self.parent.graph_order,
                reader_order=self.target.graph_order,
            )
        )
        patch_cable_synthdef = build_patch_cable(
            self.parent.effective_channel_count,
            self.target.effective_channel_count,
        )
        return [
            SynthDefSpec(
                component=self,
                context=context,
                name=patch_cable_synthdef.effective_name,
                synthdef=patch_cable_synthdef,
            ),
            SynthSpec(
                add_action=(
                    AddAction.ADD_AFTER if self.postfader else AddAction.ADD_BEFORE
                ),
                component=self,
                context=context,
                destroy_strategy={"done_action": DoneAction.FREE_SYNTH, "gate": 0},
                kwargs={
                    "active": Spec.get_address(
                        self.parent, Names.CONTROL_BUSSES, Names.ACTIVE
                    ),
                    "in_": Spec.get_address(
                        self.parent, Names.AUDIO_BUSSES, Names.MAIN
                    ),
                    "out": Spec.get_address(
                        self.target,
                        Names.AUDIO_BUSSES,
                        Names.FEEDBACK if feedsback else Names.MAIN,
                    ),
                },
                name=Names.SYNTH,
                synthdef=Spec.get_address(
                    None,
                    Names.SYNTHDEFS,
                    patch_cable_synthdef.effective_name,
                ),
                target_node=Spec.get_address(
                    self.parent, Names.NODES, Names.CHANNEL_STRIP
                ),
            ),
        ]

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            await self._reconcile(context=None, deleting=True)

    @property
    def address(self) -> Address:
        if self.parent is None:
            return "sends[?]"
        index = self.parent.sends.index(self)
        return f"{self.parent.address}.sends[{index}]"

    @property
    def numeric_address(self) -> Address:
        return f"sends[{self._id}]"

    @property
    def postfader(self) -> bool:
        return self._postfader

    @property
    def target(self) -> TrackContainer:
        return self._target


class Track(DeviceContainer[TrackContainer], TrackContainer[TrackContainer]):
    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: TrackContainer | None = None,
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)
        DeviceContainer.__init__(self)
        TrackContainer.__init__(self)
        self._cached_input: Track | None = None
        self._cached_output: TrackContainer | None = None
        self._input: BusGroup | Track | None = None
        self._output: BusGroup | Default | TrackContainer | None = DEFAULT
        self._sends: list[TrackSend] = []

    def __repr__(self) -> str:
        repr_ = super().__repr__()
        input_: str = ""
        output: str = ""
        if isinstance(self.input, Track):
            input_ = f" input={Component.__repr__(self.input)}"
        if isinstance(self.output, TrackContainer):
            output = f" output={Component.__repr__(self.output)}"
        elif self.output is None:
            output = f" output={None}"
        return f"{repr_[:-1]}{input_}{output}>"

    def _add_send(
        self,
        *,
        postfader: bool = True,
        target: TrackContainer,
    ) -> TrackSend:
        if (session := self.session) is None:
            raise RuntimeError
        if self.mixer is not target.mixer:
            raise RuntimeError
        self._sends.append(
            send := TrackSend(
                id_=session._get_next_id(),
                parent=self,
                postfader=postfader,
                target=target,
            )
        )
        return send

    def _disconnect_parentage(self) -> None:
        if (parent := self._parent) is not None and self in parent._tracks:
            parent._tracks.remove(self)
        super()._disconnect_parentage()

    def _move(self, *, parent: TrackContainer, index: int) -> None:
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

    def _notify_disconnected(self, connection: "Component") -> bool:
        if connection is self._input:
            self._input = None
        if connection is self._output:
            self._output = None
        return False

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        root: Component | None = None,
    ) -> tuple[list[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(deleting=deleting, root=root)
        old_input = self._cached_input
        old_output = self._cached_output
        if deleting:
            if self._cached_input:
                self._cached_input._connections.pop((self, Names.INPUT), None)
                related.append(self._cached_input)
            if self._cached_output:
                self._cached_output._connections.pop((self, Names.OUTPUT), None)
                related.append(self._cached_output)
        else:
            new_input: Component | None = None
            new_output: Component | None = None
            if isinstance(self._input, Track):
                new_input = self._cached_input = self._input
            if isinstance(self._output, TrackContainer):
                new_output = self._cached_output = self._output
            elif self._output is DEFAULT:
                new_output = self._cached_output = self.parent
            if old_input != new_input:
                if old_input:
                    old_input._connections.pop((self, Names.INPUT))
                if new_input:
                    new_input._connections[(self, Names.INPUT)] = IO.READ
            if old_output != new_output:
                if old_output:
                    old_output._connections.pop((self, Names.OUTPUT))
                if new_output:
                    new_output._connections[(self, Names.OUTPUT)] = IO.WRITE
            related.extend(
                sorted(
                    [
                        x
                        for x in set([old_input, old_output, new_input, new_output])
                        if x is not None
                    ],
                    key=lambda x: x.graph_order,
                )
            )
        return related, deleted

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not context:
            return []
        if not self.parent:
            raise RuntimeError
        channel_strip_synthdef = build_channel_strip(self.effective_channel_count)
        meters_synthdef = build_meters(self.effective_channel_count)
        synthdefs: list[Spec] = [
            SynthDefSpec(
                component=self,
                context=context,
                name=channel_strip_synthdef.effective_name,
                synthdef=channel_strip_synthdef,
            ),
            SynthDefSpec(
                component=self,
                context=context,
                name=meters_synthdef.effective_name,
                synthdef=meters_synthdef,
            ),
        ]
        busses: list[Spec] = [
            BusSpec(
                calculation_rate=CalculationRate.AUDIO,
                channel_count=self.effective_channel_count,
                component=self,
                context=context,
                name=Names.MAIN,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=1,
                component=self,
                context=context,
                default=1.0,
                name=Names.ACTIVE,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=1,
                component=self,
                context=context,
                default=0.0,
                name=Names.GAIN,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=self.effective_channel_count,
                component=self,
                context=context,
                default=0.0,
                name=Names.INPUT_LEVELS,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=self.effective_channel_count,
                component=self,
                context=context,
                default=0.0,
                name=Names.OUTPUT_LEVELS,
            ),
        ]
        track_index: int = self.parent.tracks.index(self)
        if track_index:
            group_add_action: AddAction = AddAction.ADD_AFTER
            group_target: Address = Spec.get_address(
                self.parent.tracks[track_index - 1],
                Names.NODES,
                Names.GROUP,
            )
        else:
            group_add_action = AddAction.ADD_TO_HEAD
            group_target = Spec.get_address(self.parent, Names.NODES, Names.TRACKS)
        groups: list[Spec] = [
            GroupSpec(
                add_action=group_add_action,
                component=self,
                context=context,
                destroy_strategy={"gate": 0},
                name=Names.GROUP,
                target_node=group_target,
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_HEAD,
                component=self,
                context=context,
                name=Names.TRACKS,
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                name=Names.DEVICES,
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
        ]
        synths: list[Spec] = [
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                destroy_strategy={
                    "done_action": DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                },
                kwargs={
                    "active": Spec.get_address(
                        self, Names.CONTROL_BUSSES, Names.ACTIVE
                    ),
                    "gain": Spec.get_address(self, Names.CONTROL_BUSSES, Names.GAIN),
                    "out": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                },
                name=Names.CHANNEL_STRIP,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, channel_strip_synthdef.effective_name
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
            SynthSpec(
                add_action=AddAction.ADD_AFTER,
                component=self,
                context=context,
                kwargs={
                    "active": Spec.get_address(
                        self, Names.CONTROL_BUSSES, Names.ACTIVE
                    ),
                    "in_": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                    "out": Spec.get_address(
                        self, Names.CONTROL_BUSSES, Names.INPUT_LEVELS
                    ),
                },
                name=Names.INPUT_LEVELS,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, meters_synthdef.effective_name
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.TRACKS),
            ),
            SynthSpec(
                add_action=AddAction.ADD_AFTER,
                component=self,
                context=context,
                kwargs={
                    "active": Spec.get_address(
                        self, Names.CONTROL_BUSSES, Names.ACTIVE
                    ),
                    "in_": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                    "out": Spec.get_address(
                        self, Names.CONTROL_BUSSES, Names.OUTPUT_LEVELS
                    ),
                },
                name=Names.OUTPUT_LEVELS,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, meters_synthdef.effective_name
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.CHANNEL_STRIP),
            ),
        ]
        if isinstance(self.input, Track):
            input_feedsback = bool(
                Spec.feedsback(
                    writer_order=self.input.graph_order,
                    reader_order=self.graph_order,
                )
            )
            input_patch_cable_synthdef = build_patch_cable(
                self.effective_channel_count,
                self.input.effective_channel_count,
                feedback=input_feedsback,
            )
            synthdefs.append(
                SynthDefSpec(
                    component=self,
                    context=context,
                    name=input_patch_cable_synthdef.effective_name,
                    synthdef=input_patch_cable_synthdef,
                )
            )
            synths.append(
                SynthSpec(
                    add_action=AddAction.ADD_TO_HEAD,
                    component=self,
                    context=context,
                    # destroy_strategy={"done_action": DoneAction.FREE_SYNTH, "gate": 0},
                    name=Names.INPUT,
                    kwargs={
                        "active": Spec.get_address(
                            self, Names.CONTROL_BUSSES, Names.ACTIVE
                        ),
                        "in_": Spec.get_address(
                            self.input,
                            Names.AUDIO_BUSSES,
                            Names.MAIN,
                        ),
                        "out": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                    },
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        input_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        if self.output is DEFAULT or isinstance(self.output, TrackContainer):
            output_target_component = (
                self.parent if self.output is DEFAULT else self.parent
            )
            output_feedsback = bool(
                Spec.feedsback(
                    writer_order=self.graph_order,
                    reader_order=output_target_component.graph_order,
                )
            )
            output_patch_cable_synthdef = build_patch_cable(
                self.effective_channel_count,
                output_target_component.effective_channel_count,
            )
            synthdefs.append(
                SynthDefSpec(
                    component=self,
                    context=context,
                    name=output_patch_cable_synthdef.effective_name,
                    synthdef=output_patch_cable_synthdef,
                )
            )
            synths.append(
                SynthSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=context,
                    # destroy_strategy={"done_action": DoneAction.FREE_SYNTH, "gate": 0},
                    name=Names.OUTPUT,
                    kwargs={
                        "active": Spec.get_address(
                            self, Names.CONTROL_BUSSES, Names.ACTIVE
                        ),
                        "in_": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                        "out": Spec.get_address(
                            output_target_component,
                            Names.AUDIO_BUSSES,
                            Names.FEEDBACK if output_feedsback else Names.MAIN,
                        ),
                    },
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        output_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        elif isinstance(self.output, BusGroup):
            output_patch_cable_synthdef = build_patch_cable(
                self.effective_channel_count,
                len(self.output),
            )
            synthdefs.append(
                SynthDefSpec(
                    component=self,
                    context=context,
                    name=output_patch_cable_synthdef.effective_name,
                    synthdef=output_patch_cable_synthdef,
                )
            )
            synths.append(
                SynthSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=context,
                    # destroy_strategy={"done_action": DoneAction.FREE_SYNTH, "gate": 0},
                    name=Names.OUTPUT,
                    kwargs={
                        "active": Spec.get_address(
                            self, Names.CONTROL_BUSSES, Names.ACTIVE
                        ),
                        "in_": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                        "out": self.output,
                    },
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        output_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        if Spec.needs_feedback(self):
            feedback_patch_cable_synthdef = build_patch_cable(
                self.effective_channel_count,
                self.effective_channel_count,
                feedback=True,
            )
            synthdefs.append(
                SynthDefSpec(
                    component=self,
                    context=context,
                    name=feedback_patch_cable_synthdef.effective_name,
                    synthdef=feedback_patch_cable_synthdef,
                )
            )
            busses.append(
                BusSpec(
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=context,
                    name=Names.FEEDBACK,
                )
            )
            synths.append(
                SynthSpec(
                    add_action=AddAction.ADD_TO_HEAD,
                    component=self,
                    context=context,
                    destroy_strategy={"gate": 0},
                    name=Names.FEEDBACK,
                    kwargs={
                        "active": Spec.get_address(
                            self, Names.CONTROL_BUSSES, Names.ACTIVE
                        ),
                        "in_": Spec.get_address(
                            self, Names.AUDIO_BUSSES, Names.FEEDBACK
                        ),
                        "out": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                    },
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        feedback_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        return synthdefs + busses + groups + synths

    async def add_send(
        self, target: TrackContainer, postfader: bool = True
    ) -> TrackSend:
        async with self._lock:
            send = self._add_send(
                postfader=postfader,
                target=target,
            )
            if context := self._can_allocate():
                await send._reconcile(context=context)
            else:
                send._reconcile_connections()
            return send

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            await self._reconcile(context=None, deleting=True)

    async def move(self, parent: TrackContainer, index: int) -> None:
        async with self._lock:
            self._move(parent=parent, index=index)
            if context := self._can_allocate():
                await self._reconcile(context=context)

    async def set_input(self, input_: Union[BusGroup, "Track"] | None) -> None:
        async with self._lock:
            if input_ is self:
                raise RuntimeError
            elif isinstance(input_, Track) and input_.mixer is not self.mixer:
                raise RuntimeError
            self._input = input_
            if context := self._can_allocate():
                await self._reconcile(context=context)
            else:
                self._reconcile_connections()

    async def set_output(
        self, output: Union[BusGroup, Default, TrackContainer] | None
    ) -> None:
        async with self._lock:
            if output is self:
                raise RuntimeError
            elif isinstance(output, TrackContainer) and output.mixer is not self.mixer:
                raise RuntimeError
            self._output = output
            if context := self._can_allocate():
                await self._reconcile(context=context)
            else:
                self._reconcile_connections()

    async def set_muted(self, muted: bool) -> None:
        async with self._lock:
            raise NotImplementedError

    def set_name(self, name: str | None = None) -> None:
        self._name = name

    async def set_soloed(self, soloed: bool) -> None:
        async with self._lock:
            raise NotImplementedError

    async def ungroup(self) -> None:
        async with self._lock:
            raise NotImplementedError

    @property
    def address(self) -> Address:
        if self.parent is None:
            return "tracks[?]"
        index = self.parent.tracks.index(self)
        return f"{self.parent.address}.tracks[{index}]"

    @property
    def children(self) -> list[Component]:
        return [*self._tracks, *self._devices, *self._sends]

    @property
    def input(self) -> Union[BusGroup, "Track"] | None:
        return self._input

    @property
    def input_levels(self) -> list[float]:
        raise NotImplementedError

    @property
    def is_active(self) -> bool:
        raise NotImplementedError

    @property
    def numeric_address(self) -> Address:
        return f"tracks[{self._id}]"

    @property
    def output(self) -> Union[BusGroup, Default, TrackContainer] | None:
        return self._output

    @property
    def output_levels(self) -> list[float]:
        raise NotImplementedError

    @property
    def sends(self) -> list[TrackSend]:
        return [*self._sends]
