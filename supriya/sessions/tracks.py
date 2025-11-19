from typing import TYPE_CHECKING, Iterable, Optional, Union

from ..contexts import BusGroup
from ..enums import AddAction, DoneAction
from ..typing import INHERIT, Inherit
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
from .constants import Address, Entities, Names
from .devices import DeviceContainer
from .parameters import FloatField
from .routing import Input, Output
from .specs import (
    Spec,
    SpecFactory,
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
        self._add_parameter(
            name=Names.GAIN,
            has_bus=True,
            field=FloatField(),
        )
        self._output = Output(
            add_action=AddAction.ADD_AFTER if self._postfader else AddAction.ADD_BEFORE,
            add_node_address=lambda component: Spec.get_address(
                component._ensure_parent(),
                Entities.NODES,
                Names.CHANNEL_STRIP,
            ),
            destroy_strategy=dict(done_action=DoneAction.FREE_SYNTH, gate=0),
            host_component=self,
            kwargs=dict(
                active=lambda component: Spec.get_address(
                    component._ensure_parent(), Entities.CONTROL_BUSES, Names.ACTIVE
                ),
                gain=Spec.get_address(self, Entities.CONTROL_BUSES, Names.GAIN),
            ),
            name=Names.SYNTH,
            source=lambda component: component._ensure_parent(),
            source_bus_address=lambda component: Spec.get_address(
                component._ensure_parent(), Entities.AUDIO_BUSES, Names.MAIN
            ),
            target=target,
        )

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

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "sends[?]"
        index = self.parent.sends.index(self)
        return f"{self.parent.address}.sends[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"sends[{self._id}]"

    def _on_connection_deleted(self, connection: "Component") -> bool:
        return connection is self._output._target

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: list[Component] | None = None,
    ) -> tuple[set[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(
            deleting=deleting, roots=roots
        )
        related.update(self._output._reconcile_connections(deleting=deleting))
        return related, deleted

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        for parameter in self.parameters.values():
            parameter._resolve_specs(spec_factory)
        self._output._resolve_specs(spec_factory)
        return spec_factory

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
        assert isinstance(target := self._output._target, TrackContainer)
        return target


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
            add_node_address=Spec.get_address(self, Entities.NODES, Names.GROUP),
            add_action=AddAction.ADD_TO_HEAD,
            host_component=self,
            kwargs=dict(
                active=Spec.get_address(self, Entities.CONTROL_BUSES, Names.ACTIVE),
            ),
            name=Names.INPUT,
            target_bus_address=Spec.get_address(self, Entities.AUDIO_BUSES, Names.MAIN),
        )
        self._is_muted: bool = False
        self._is_soloed: bool = False
        self._output = Output(
            add_action=AddAction.ADD_TO_TAIL,
            add_node_address=Spec.get_address(self, Entities.NODES, Names.GROUP),
            host_component=self,
            kwargs=dict(
                active=Spec.get_address(self, Entities.CONTROL_BUSES, Names.ACTIVE),
            ),
            name=Names.OUTPUT,
            source_bus_address=Spec.get_address(self, Entities.AUDIO_BUSES, Names.MAIN),
            target=INHERIT,
        )
        self._sends: list[TrackSend] = []
        self._add_parameter(
            name=Names.GAIN,
            has_bus=True,
            field=FloatField(),
        )

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
        if (
            active_bus := self._local_artifacts.control_buses.get(Names.ACTIVE)
        ) is None:
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

    def _disconnect_parentage(self) -> None:
        self._ensure_parent()._unsolo_tracks(tracks=self._soloed_tracks)
        self._ensure_parent()._tracks.remove(self)

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

    def _on_connection_deleted(self, connection: "Component") -> bool:
        self._input._on_connection_deleted(connection)
        self._output._on_connection_deleted(connection)
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
    ) -> tuple[set[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(
            deleting=deleting, roots=roots
        )
        related.update(self._input._reconcile_connections(deleting=deleting))
        related.update(self._output._reconcile_connections(deleting=deleting))
        return related, deleted

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        # cache
        effective_channel_count = self.effective_channel_count
        # parameters
        for parameter in self.parameters.values():
            parameter._resolve_specs(spec_factory)
        # synthdefs
        channel_strip_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_channel_strip_synthdef(effective_channel_count)
        )
        meters_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_meters_synthdef(effective_channel_count)
        )
        # audio buses
        main_audio_bus_address = spec_factory.add_audio_bus(
            channel_count=effective_channel_count,
            name=Names.MAIN,
        )
        # control buses
        active_control_bus_address = spec_factory.add_control_bus(
            channel_count=1,
            default=float(self._is_active),
            name=Names.ACTIVE,
        )
        input_levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            default=0.0,
            name=Names.INPUT_LEVELS,
        )
        output_levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            default=0.0,
            name=Names.OUTPUT_LEVELS,
        )
        # groups
        parent = self._ensure_parent()
        container_group_address = spec_factory.add_container_group(
            destroy_strategy={"gate": 0},
            parent=(parent := self._ensure_parent()),
            parent_container=parent.tracks,
            parent_container_group_name=Names.TRACKS,
        )
        tracks_group_address = spec_factory.add_group(
            add_action=AddAction.ADD_TO_HEAD,
            name=Names.TRACKS,
            target_node=container_group_address,
        )
        _ = spec_factory.add_group(
            add_action=AddAction.ADD_TO_TAIL,
            name=Names.DEVICES,
            target_node=container_group_address,
        )
        # synths
        channel_strip_synth_address = spec_factory.add_synth(
            add_action=AddAction.ADD_TO_TAIL,
            destroy_strategy=dict(
                done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
            ),
            kwargs=dict(
                active=active_control_bus_address,
                gain=Spec.get_address(self, Entities.CONTROL_BUSES, Names.GAIN),
                out=main_audio_bus_address,
            ),
            name=Names.CHANNEL_STRIP,
            synthdef=channel_strip_synthdef_address,
            target_node=container_group_address,
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_AFTER,
            kwargs=dict(
                active=active_control_bus_address,
                in_=main_audio_bus_address,
                out=input_levels_control_bus_address,
            ),
            name=Names.INPUT_LEVELS,
            synthdef=meters_synthdef_address,
            target_node=tracks_group_address,
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_AFTER,
            kwargs=dict(
                active=active_control_bus_address,
                in_=main_audio_bus_address,
                out=output_levels_control_bus_address,
            ),
            name=Names.OUTPUT_LEVELS,
            synthdef=meters_synthdef_address,
            target_node=channel_strip_synth_address,
        )
        # conditional synths
        self._input._resolve_specs(spec_factory)
        self._output._resolve_specs(spec_factory)
        if Spec.needs_feedback(self):
            feedback_patch_cable_synthdef_address = spec_factory.add_synthdef(
                synthdef=build_patch_cable_synthdef(
                    effective_channel_count,
                    effective_channel_count,
                    feedback=True,
                )
            )
            feedback_audio_bus_address = spec_factory.add_audio_bus(
                channel_count=effective_channel_count,
                name=Names.FEEDBACK,
            )
            spec_factory.add_synth(
                add_action=AddAction.ADD_TO_HEAD,
                destroy_strategy=dict(gate=0),
                name=Names.FEEDBACK,
                kwargs=dict(
                    active=active_control_bus_address,
                    in_=feedback_audio_bus_address,
                    out=main_audio_bus_address,
                ),
                synthdef=feedback_patch_cable_synthdef_address,
                target_node=container_group_address,
            )
        return spec_factory

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
        self, output: Union[BusGroup, Inherit, TrackContainer] | None
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
    def output(self) -> Union[BusGroup, Inherit, TrackContainer] | None:
        """
        Get the track's audio output destination.
        """
        if (output := self._output._target) is not None:
            assert isinstance(output, (BusGroup, Inherit, TrackContainer))
        return output

    @property
    def sends(self) -> list[TrackSend]:
        """
        Get the track's track sends.
        """
        return [*self._sends]
