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
    ChannelSettable,
    Component,
    Deletable,
    LevelsCheckable,
    Movable,
    NameSettable,
)
from .constants import IO, Address, Names
from .devices import DeviceContainer
from .parameters import FloatField
from .routing import Input, Output
from .specs import (
    BusSpec,
    GroupSpec,
    Spec,
    Specs,
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

    def _group_tracks(self, index: int, count: int, name: str | None = None) -> "Track":
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
        self, index: int, count: int, *, name: str | None = None
    ) -> "Track":
        """
        Group one or more tracks in the track container as subtracks of a new track.
        """
        async with (session := self._ensure_session())._lock:
            track = self._group_tracks(index=index, count=count, name=name)
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


class TrackSend(Deletable["Track"]):
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
        self._add_parameter(name=Names.GAIN, field=FloatField(has_bus=True))

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

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        specs = Specs()
        if not context:
            return specs
        parent = self._ensure_parent()
        feedsback = bool(
            Spec.feedsback(
                writer_order=parent.graph_order,
                reader_order=self.target.graph_order,
            )
        )
        for parameter in self.parameters.values():
            specs.update(parameter._resolve_specs(context=context))
        specs.synthdef_specs.append(
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
            )
        )
        specs.synth_specs.append(
            SynthSpec(
                add_action=(
                    AddAction.ADD_AFTER if self.postfader else AddAction.ADD_BEFORE
                ),
                component=self,
                context=context,
                destroy_strategy={"done_action": DoneAction.FREE_SYNTH, "gate": 0},
                kwargs={
                    "active": Spec.get_address(
                        parent, Names.CONTROL_BUSES, Names.ACTIVE
                    ),
                    "gain": Spec.get_address(self, Names.CONTROL_BUSES, Names.GAIN),
                    "in_": Spec.get_address(parent, Names.AUDIO_BUSES, Names.MAIN),
                    "out": Spec.get_address(
                        self.target,
                        Names.AUDIO_BUSES,
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
                target_node=Spec.get_address(parent, Names.NODES, Names.CHANNEL_STRIP),
            )
        )
        return specs

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


class Track(
    DeviceContainer[TrackContainer],
    TrackContainer,
    ChannelSettable,
    Deletable,
    LevelsCheckable,
    Movable,
    NameSettable,
):
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
        self._cached_output: TrackContainer | None = None
        self._input = Input(
            add_node_address=Spec.get_address(self, Names.NODES, Names.GROUP),
            add_action=AddAction.ADD_TO_HEAD,
            host_component=self,
            kwargs=dict(
                active=Spec.get_address(self, Names.CONTROL_BUSES, Names.ACTIVE),
            ),
            name=Names.INPUT,
            target_bus_name=Names.MAIN,
        )
        self._is_muted: bool = False
        self._is_soloed: bool = False
        self._output = Output(
            add_action=AddAction.ADD_TO_TAIL,
            add_node_address=Spec.get_address(self, Names.NODES, Names.GROUP),
            host_component=self,
            kwargs=dict(
                active=Spec.get_address(self, Names.CONTROL_BUSES, Names.ACTIVE),
            ),
            name=Names.OUTPUT,
            source_bus_address=Spec.get_address(self, Names.AUDIO_BUSES, Names.MAIN),
            target=DEFAULT,
        )
        self._sends: list[TrackSend] = []
        self._add_parameter(name=Names.GAIN, field=FloatField(has_bus=True))

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
        self._input._notify_disconnected(connection)
        self._output._notify_disconnected(connection)
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
        related.extend(self._input._reconcile_connections(deleting=deleting))
        related.extend(self._output._reconcile_connections(deleting=deleting))
        return sorted(set(related), key=lambda x: x.graph_order), deleted

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        specs = Specs()
        if not context:
            return specs
        parent = self._ensure_parent()
        for parameter in self.parameters.values():
            specs.update(parameter._resolve_specs(context=context))
        channel_strip_synthdef = build_channel_strip_synthdef(
            self.effective_channel_count
        )
        meters_synthdef = build_meters_synthdef(self.effective_channel_count)
        specs.synthdef_specs.extend(
            [
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
        )
        specs.bus_specs.extend(
            [
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
        )
        specs.group_specs.extend(
            [
                self._resolve_container_spec(
                    context=context,
                    destroy_strategy={"gate": 0},
                    parent=(parent := self._ensure_parent()),
                    parent_container=parent.tracks,
                    parent_container_group_name=Names.TRACKS,
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
        )
        specs.synth_specs.extend(
            [
                SynthSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=context,
                    destroy_strategy={
                        "done_action": DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                    },
                    kwargs={
                        "active": Spec.get_address(
                            self, Names.CONTROL_BUSES, Names.ACTIVE
                        ),
                        "gain": Spec.get_address(self, Names.CONTROL_BUSES, Names.GAIN),
                        "out": Spec.get_address(self, Names.AUDIO_BUSES, Names.MAIN),
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
                            self, Names.CONTROL_BUSES, Names.ACTIVE
                        ),
                        "in_": Spec.get_address(self, Names.AUDIO_BUSES, Names.MAIN),
                        "out": Spec.get_address(
                            self, Names.CONTROL_BUSES, Names.INPUT_LEVELS
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
                            self, Names.CONTROL_BUSES, Names.ACTIVE
                        ),
                        "in_": Spec.get_address(self, Names.AUDIO_BUSES, Names.MAIN),
                        "out": Spec.get_address(
                            self, Names.CONTROL_BUSES, Names.OUTPUT_LEVELS
                        ),
                    },
                    name=Names.OUTPUT_LEVELS,
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None, Names.SYNTHDEFS, meters_synthdef.effective_name
                    ),
                    target_node=Spec.get_address(
                        self, Names.NODES, Names.CHANNEL_STRIP
                    ),
                ),
            ]
        )
        specs.update(self._input._resolve_specs(context))
        specs.update(self._output._resolve_specs(context))
        if Spec.needs_feedback(self):
            feedback_patch_cable_synthdef = build_patch_cable_synthdef(
                self.effective_channel_count,
                self.effective_channel_count,
                feedback=True,
            )
            specs.synthdef_specs.append(
                SynthDefSpec(
                    component=self,
                    context=context,
                    name=feedback_patch_cable_synthdef.effective_name,
                    synthdef=feedback_patch_cable_synthdef,
                )
            )
            specs.bus_specs.append(
                BusSpec(
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=context,
                    name=Names.FEEDBACK,
                )
            )
            specs.synth_specs.append(
                SynthSpec(
                    add_action=AddAction.ADD_TO_HEAD,
                    component=self,
                    context=context,
                    destroy_strategy={"gate": 0},
                    name=Names.FEEDBACK,
                    kwargs={
                        "active": Spec.get_address(
                            self, Names.CONTROL_BUSES, Names.ACTIVE
                        ),
                        "in_": Spec.get_address(
                            self, Names.AUDIO_BUSES, Names.FEEDBACK
                        ),
                        "out": Spec.get_address(self, Names.AUDIO_BUSES, Names.MAIN),
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

    async def set_input(self, input_: Union[BusGroup, "Track"] | None) -> None:
        """
        Set the track's audio input source.
        """
        async with (session := self._ensure_session())._lock:
            if input_ is self:
                raise RuntimeError
            elif isinstance(input_, Track) and input_.mixer is not self.mixer:
                raise RuntimeError
            self._input.set(input_)
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
            self._output.set(output)
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
        if (input_ := self._input._source) is not None:
            assert isinstance(input_, (BusGroup, Track))
        return input_

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
        if (output := self._output._target) is not None:
            assert isinstance(output, (BusGroup, Default, TrackContainer))
        return output

    @property
    def sends(self) -> list[TrackSend]:
        """
        Get the track's track sends.
        """
        return [*self._sends]
