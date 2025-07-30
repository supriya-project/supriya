from typing import TYPE_CHECKING, Iterable, Optional, Union

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction, CalculationRate, DoneAction
from ..typing import DEFAULT, Default
from ..ugens.system import (
    build_channel_strip_synthdef,
    build_meters_synthdef,
    build_patch_cable_synthdef,
)
from .components import (
    Component,
)
from .constants import IO, Address, ChannelCount, Names
from .devices import DeviceContainer
from .specs import (
    BusSpec,
    GroupSpec,
    Spec,
    SynthDefSpec,
    SynthSpec,
)

if TYPE_CHECKING:
    from .sessions import Session


class TrackContainer(Component[Union["Session", "TrackContainer"]]):
    """
    A container for track components.

    Supports adding tracks and grouping them.
    """

    def __init__(self) -> None:
        self._tracks: list[Track] = []
        self._soloed_tracks: set[Track] = set()

    def _add_track(self, name: str | None = None) -> "Track":
        self._tracks.append(
            track := Track(
                id_=self._ensure_session()._get_next_id(), name=name, parent=self
            )
        )
        return track

    def _solo_track(
        self,
        *,
        exclusive: bool,
        track: "Track",
    ) -> None:
        # TODO: Can these be consolidated into a TrackSoloContext?
        if exclusive:
            self._soloed_tracks.clear()
        self._soloed_tracks.add(track)
        self._ensure_parent()._solo_track(
            exclusive=exclusive,
            track=track,
        )

    def _solo_tracks(self, *, tracks: Iterable["Track"]) -> None:
        # TODO: Can these be consolidated into a TrackSoloContext?
        self._soloed_tracks.update(tracks)
        self._ensure_parent()._solo_tracks(tracks=tracks)

    def _unsolo_tracks(self, *, tracks: Iterable["Track"]) -> None:
        # TODO: Can these be consolidated into a TrackSoloContext?
        self._soloed_tracks -= set(tracks)
        self._ensure_parent()._unsolo_tracks(tracks=tracks)

    def _group(self, index: int, count: int, name: str | None = None) -> "Track":
        if index < 0:
            raise RuntimeError(index)
        elif count < 1:
            raise RuntimeError(count)
        elif (index + count) > len(self.tracks):
            raise RuntimeError(index, count)
        group_track = Track(
            id_=self._ensure_session()._get_next_id(), name=name, parent=self
        )
        child_tracks = self._tracks[index : index + count]
        group_track._tracks[:] = child_tracks
        self._tracks[index : index + count] = [group_track]
        for track in child_tracks:
            track._parent = group_track
        return group_track

    async def add_track(self, name: str | None = None) -> "Track":
        """
        Add a new track to the track container.
        """
        async with (session := self._ensure_session())._lock:
            track = self._add_track(name=name)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[track],
                session=session,
            )
            return track

    async def group_tracks(
        self, index: int, count: int, name: str | None = None
    ) -> "Track":
        """
        Group one or more tracks in the track container as subtracks of a new track.
        """
        async with (session := self._ensure_session())._lock:
            track = self._group(index=index, count=count, name=name)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[track],
                session=session,
            )
            return track

    @property
    def tracks(self) -> list["Track"]:
        """
        Get the track container's tracks.
        """
        return self._tracks[:]


class TrackSend(Component["Track"]):
    """
    A track send

    Sends audio from one track to another track container (e.g. another track
    or mixer).
    """

    # TODO: Test signal routing.

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
        self._add_parameter(name=Names.GAIN)

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
        self._ensure_parent()._sends.remove(self)
        super()._disconnect_parentage()

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "sends[?]"
        index = self.parent.sends.index(self)
        return f"{self.parent.address}.sends[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"sends[{self._id}]"

    def _notify_disconnected(self, connection: "Component") -> bool:
        return connection is self._target

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: list[Component] | None = None,
    ) -> tuple[list[Component], set[Component]]:
        parent = self._ensure_parent()
        related, deleted = super()._reconcile_connections(
            deleting=deleting, roots=roots
        )
        components: list[Component] = [parent, self.target]
        if deleting:
            parent._connections.pop((self, Names.INPUT), None)
            self.target._connections.pop((self, Names.OUTPUT), None)
        else:
            parent._connections[(self, Names.INPUT)] = IO.READ
            self.target._connections[(self, Names.OUTPUT)] = IO.WRITE
        related.extend(sorted(components, key=lambda x: x.graph_order))
        return related, deleted

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not context:
            return []
        parent = self._ensure_parent()
        feedsback = bool(
            Spec.feedsback(
                writer_order=parent.graph_order,
                reader_order=self.target.graph_order,
            )
        )
        specs = []
        for parameter in self.parameters.values():
            specs.extend(parameter._resolve_specs(context=context))
        specs.extend(
            [
                SynthDefSpec(
                    component=self,
                    context=context,
                    name=(
                        patch_cable_synthdef := build_patch_cable_synthdef(
                            parent.effective_channel_count,
                            self.target.effective_channel_count,
                        )
                    ).effective_name,
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
                            parent, Names.CONTROL_BUSSES, Names.ACTIVE
                        ),
                        "gain": Spec.get_address(
                            self, Names.CONTROL_BUSSES, Names.GAIN
                        ),
                        "in_": Spec.get_address(parent, Names.AUDIO_BUSSES, Names.MAIN),
                        "out": Spec.get_address(
                            self.target,
                            Names.AUDIO_BUSSES,
                            Names.FEEDBACK if feedsback else Names.MAIN,
                        ),
                    },
                    name=Names.SYNTH,
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(
                        parent, Names.NODES, Names.CHANNEL_STRIP
                    ),
                ),
            ]
        )
        return specs

    async def delete(self) -> None:
        """
        Delete the send.
        """
        async with (session := self._ensure_session())._lock:
            await Component._reconcile(
                context=None,
                deleting_components=[self],
                reconciling_components=[self],
                session=session,
            )

    @property
    def feedback_graph_order(self) -> tuple[int, ...]:
        """
        Get the send's graph order for sake of feedback calculations.
        """
        return self._ensure_parent().graph_order

    @property
    def postfader(self) -> bool:
        """
        Get the send's pre/post-fader status.
        """
        return self._postfader

    @property
    def target(self) -> TrackContainer:
        """
        Get the send's target track container.
        """
        return self._target


class Track(DeviceContainer[TrackContainer], TrackContainer):
    """
    A track component.
    """

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
        self._is_muted: bool = False
        self._is_soloed: bool = False
        self._output: BusGroup | Default | TrackContainer | None = DEFAULT
        self._sends: list[TrackSend] = []
        self._add_parameter(name=Names.GAIN)

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

    def _apply_activation(self) -> None:
        if (active_bus := self._artifacts.control_buses.get(Names.ACTIVE)) is None:
            return
        active_bus.set(float(self._is_active))

    def _add_send(
        self,
        *,
        name: str | None = None,
        postfader: bool = True,
        target: TrackContainer,
    ) -> TrackSend:
        if self.mixer is not target.mixer:
            raise RuntimeError
        self._sends.append(
            send := TrackSend(
                id_=self._ensure_session()._get_next_id(),
                name=name,
                parent=self,
                postfader=postfader,
                target=target,
            )
        )
        return send

    def _delete(self) -> None:
        self._ensure_parent()._unsolo_tracks(tracks=self._soloed_tracks)
        super()._delete()

    def _disconnect_parentage(self) -> None:
        self._ensure_parent()._tracks.remove(self)
        super()._disconnect_parentage()

    def _move(self, *, new_parent: TrackContainer, index: int) -> None:
        # Validate if moving is possible
        if self.mixer is not new_parent.mixer:
            raise RuntimeError
        elif self in new_parent.parentage:
            raise RuntimeError
        elif index < 0:
            raise RuntimeError
        elif index and index >= len(new_parent.tracks):
            raise RuntimeError
        # Reconfigure parentage and bail if this is a no-op
        old_parent = self._ensure_parent()
        old_index = old_parent._tracks.index(self)
        if old_parent is new_parent and old_index == index:
            return  # Bail
        old_parent._tracks.remove(self)
        self._parent = new_parent
        new_parent._tracks.insert(index, self)
        if old_parent is not new_parent:
            old_parent._unsolo_tracks(tracks=self._soloed_tracks)
            new_parent._solo_tracks(tracks=self._soloed_tracks)

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "tracks[?]"
        index = self.parent.tracks.index(self)
        return f"{self.parent.address}.tracks[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"tracks[{self._id}]"

    def _notify_disconnected(self, connection: "Component") -> bool:
        if connection is self._input:
            self._input = None
        if connection is self._output:
            self._output = None
        return False

    def _reconcile_activation(self) -> bool:
        cached_is_active = self._is_active
        if self._is_muted:
            self._is_active = False
        elif self._is_soloed:
            self._is_active = True
        elif self.session and (soloed_tracks := self.session._soloed_tracks):
            if self._soloed_tracks:
                self._is_active = True
            else:
                for parent in self.parentage:
                    if parent in soloed_tracks:
                        self._is_active = True
                        break
                else:
                    self._is_active = False
        else:
            self._is_active = True
        # return True if changed
        return self._is_active != cached_is_active

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: list[Component] | None = None,
    ) -> tuple[list[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(
            deleting=deleting, roots=roots
        )
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
        parent = self._ensure_parent()
        specs = []
        for parameter in self.parameters.values():
            specs.extend(parameter._resolve_specs(context=context))
        channel_strip_synthdef = build_channel_strip_synthdef(
            self.effective_channel_count
        )
        meters_synthdef = build_meters_synthdef(self.effective_channel_count)
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
        buses: list[Spec] = [
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
                default=float(self._is_active),
                name=Names.ACTIVE,
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
        track_index: int = parent.tracks.index(self)
        if track_index:
            group_add_action: AddAction = AddAction.ADD_AFTER
            group_target: Address = Spec.get_address(
                parent.tracks[track_index - 1],
                Names.NODES,
                Names.GROUP,
            )
        else:
            group_add_action = AddAction.ADD_TO_HEAD
            group_target = Spec.get_address(parent, Names.NODES, Names.TRACKS)
        groups: list[Spec] = [
            GroupSpec(
                add_action=group_add_action,
                component=self,
                context=context,
                destroy_strategy={"gate": 0},
                name=Names.GROUP,
                parent_node=Spec.get_address(parent, Names.NODES, Names.TRACKS),
                target_node=group_target,
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_HEAD,
                component=self,
                context=context,
                name=Names.TRACKS,
                parent_node=None,
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                name=Names.DEVICES,
                parent_node=None,
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
                parent_node=None,
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
                parent_node=None,
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
                parent_node=None,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, meters_synthdef.effective_name
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.CHANNEL_STRIP),
            ),
        ]
        if isinstance(self.input, Track):
            input_feedsback = bool(
                Spec.feedsback(
                    writer_order=self.input.feedback_graph_order,
                    reader_order=self.graph_order,
                )
            )
            input_patch_cable_synthdef = build_patch_cable_synthdef(
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
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        input_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        if self.output is DEFAULT or isinstance(self.output, TrackContainer):
            output_target_component = parent if self.output is DEFAULT else self.output
            assert isinstance(output_target_component, TrackContainer)
            output_feedsback = bool(
                Spec.feedsback(
                    writer_order=self.feedback_graph_order,
                    reader_order=output_target_component.graph_order,
                )
            )
            output_patch_cable_synthdef = build_patch_cable_synthdef(
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
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        output_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        elif isinstance(self.output, BusGroup):
            output_patch_cable_synthdef = build_patch_cable_synthdef(
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
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        output_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        if Spec.needs_feedback(self):
            feedback_patch_cable_synthdef = build_patch_cable_synthdef(
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
            buses.append(
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
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        feedback_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                )
            )
        specs.extend(synthdefs + buses + groups + synths)
        return specs

    def _set_muted(self, *, muted: bool) -> None:
        self._is_muted = bool(muted)

    def _set_soloed(self, *, soloed: bool, exclusive: bool = True) -> None:
        self._is_soloed = bool(soloed)
        if self._is_soloed:
            self._solo_track(
                exclusive=exclusive,
                track=self,
            )
        else:
            self._unsolo_tracks(tracks=[self])

    def _ungroup(self) -> list["Track"]:
        parent = self._ensure_parent()
        if not self.tracks:
            raise RuntimeError
        index = parent.tracks.index(self)
        tracks = self.tracks[:]
        parent._tracks[index + 1 : index + 1] = tracks
        for track in tracks:
            track._parent = parent
        self._tracks[:] = []
        return tracks

    async def add_send(
        self,
        *,
        name: str | None = None,
        postfader: bool = True,
        target: TrackContainer,
    ) -> TrackSend:
        """
        Add a send to the track.
        """
        async with (session := self._ensure_session())._lock:
            send = self._add_send(
                name=name,
                postfader=postfader,
                target=target,
            )
            await Component._reconcile(
                context=self.context,
                reconciling_components=[send],
                session=session,
            )
            return send

    async def delete(self) -> None:
        """
        Delete the track.
        """
        async with (session := self._ensure_session())._lock:
            await Component._reconcile(
                context=None,
                deleting_components=[self],
                reconciling_components=[self],
                session=session,
            )

    async def move(self, parent: TrackContainer, index: int) -> None:
        """
        Move the track to another track container and/or index in a track
        container.
        """
        async with (session := self._ensure_session())._lock:
            self._move(new_parent=parent, index=index)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    async def set_channel_count(self, channel_count: ChannelCount | Default) -> None:
        """
        Set the tracks's channel count.
        """
        async with (session := self._ensure_session())._lock:
            self._channel_count = channel_count
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    async def set_input(self, input_: Union[BusGroup, "Track"] | None) -> None:
        """
        Set the track's audio input source.
        """
        async with (session := self._ensure_session())._lock:
            if input_ is self:
                raise RuntimeError
            elif isinstance(input_, Track) and input_.mixer is not self.mixer:
                raise RuntimeError
            self._input = input_
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    async def set_muted(self, muted: bool) -> None:
        """
        Set the track's mute status.
        """
        # TODO: Test this.
        async with self._ensure_session()._lock:
            self._set_muted(muted=muted)
            if self._reconcile_activation():
                self._apply_activation()

    def set_name(self, name: str | None = None) -> None:
        """
        Set the track's name.
        """
        self._name = name

    async def set_output(
        self, output: Union[BusGroup, Default, TrackContainer] | None
    ) -> None:
        """
        Set the track's audio output destination.
        """
        async with (session := self._ensure_session())._lock:
            if output is self:
                raise RuntimeError
            elif isinstance(output, TrackContainer) and output.mixer is not self.mixer:
                raise RuntimeError
            self._output = output
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    async def set_soloed(self, soloed: bool, exclusive: bool = True) -> None:
        """
        Set the track's solo status.

        If soloing, unsolo any other soloed tracks unless ``exclusive`` has been set to ``False``.
        """
        async with (session := self._ensure_session())._lock:
            self._set_soloed(soloed=soloed, exclusive=exclusive)
            session._update_track_activation()

    async def ungroup(self) -> None:
        """
        Ungroup the track.

        Replace the track in its parent with the group track's children.
        """
        async with (session := self._ensure_session())._lock:
            tracks = self._ungroup()
            await Component._reconcile(
                context=self.context,
                deleting_components=[self],
                reconciling_components=[self, *tracks],
                session=session,
            )

    @property
    def children(self) -> list[Component]:
        """
        Get the track's child components.
        """
        return [*self._tracks, *self._devices, *self._sends]

    @property
    def input(self) -> Union[BusGroup, "Track"] | None:
        """
        Get the track's audio input source.
        """
        return self._input

    @property
    def input_levels(self) -> list[float]:
        """
        Get the track's current input levels.

        Read from server shared memory.
        """
        # TODO: Test this.
        if not (shared_memory := self._ensure_context()._shared_memory):
            raise RuntimeError
        return shared_memory[self._artifacts.control_buses[Names.INPUT_LEVELS]]

    @property
    def is_active(self) -> bool:
        """
        Get the track's active status, as computed from its mute and solo states.
        """
        return self._is_active

    @property
    def is_muted(self) -> bool:
        """
        Get the track's mute status.
        """
        return self._is_muted

    @property
    def is_soloed(self) -> bool:
        """
        Get the track's solo status.
        """
        return self._is_soloed

    @property
    def output(self) -> Union[BusGroup, Default, TrackContainer] | None:
        """
        Get the track's audio output destination.
        """
        return self._output

    @property
    def output_levels(self) -> list[float]:
        """
        Get the track's current output levels.

        Read from server shared memory.
        """
        # TODO: Test this.
        if not (shared_memory := self._ensure_context()._shared_memory):
            raise RuntimeError
        return shared_memory[self._artifacts.control_buses[Names.OUTPUT_LEVELS]]

    @property
    def sends(self) -> list[TrackSend]:
        """
        Get the track's track sends.
        """
        return [*self._sends]
