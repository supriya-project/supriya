import dataclasses
from typing import Union

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction, CalculationRate
from ..typing import DEFAULT, Default
from .components import (
    C,
    ChannelCount,
    Component,
    Names,
    State,
)
from .specs import (
    Address,
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
            return track

    async def group(self, index: int, count: int) -> "Track":
        async with self._lock:
            return self._group(index=index, count=count)

    @property
    def tracks(self) -> list["Track"]:
        return self._tracks[:]


@dataclasses.dataclass
class TrackState(State):
    channel_count: ChannelCount = 2

    def resolve_specs(
        self, component: Component, context: AsyncServer | None
    ) -> list[Spec]:
        if not context:
            return []
        if not component.parent:
            raise RuntimeError
        if not isinstance(component, Track):
            raise RuntimeError
        channel_strip_synthdef = build_channel_strip(self.channel_count)
        meters_synthdef = build_meters(self.channel_count)
        specs: list[Spec] = [
            SynthDefSpec(
                component=component,
                context=context,
                name=channel_strip_synthdef.effective_name,
                synthdef=channel_strip_synthdef,
            ),
            SynthDefSpec(
                component=component,
                context=context,
                name=meters_synthdef.effective_name,
                synthdef=meters_synthdef,
            ),
            BusSpec(
                calculation_rate=CalculationRate.AUDIO,
                channel_count=self.channel_count,
                component=component,
                context=context,
                name=Names.MAIN,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=1,
                component=component,
                context=context,
                default=1.0,
                name=Names.ACTIVE,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=1,
                component=component,
                context=context,
                default=0.0,
                name=Names.GAIN,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=self.channel_count,
                component=component,
                context=context,
                default=0.0,
                name=Names.INPUT_LEVELS,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=self.channel_count,
                component=component,
                context=context,
                default=0.0,
                name=Names.OUTPUT_LEVELS,
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=component,
                context=context,
                name=Names.GROUP,
                # TODO: Need more advanced logic here for positioning
                target_node=Spec.get_address(
                    component.parent, Names.NODES, Names.TRACKS
                ),
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_HEAD,
                component=component,
                context=context,
                name=Names.TRACKS,
                target_node=Spec.get_address(component, Names.NODES, Names.GROUP),
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=component,
                context=context,
                name=Names.DEVICES,
                target_node=Spec.get_address(component, Names.NODES, Names.GROUP),
            ),
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=component,
                context=context,
                kwargs={
                    "active": Spec.get_address(
                        component, Names.CONTROL_BUSSES, Names.ACTIVE
                    ),
                    "gain": Spec.get_address(
                        component, Names.CONTROL_BUSSES, Names.GAIN
                    ),
                    "out": Spec.get_address(component, Names.AUDIO_BUSSES, Names.MAIN),
                },
                name=Names.CHANNEL_STRIP,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, channel_strip_synthdef.effective_name
                ),
                target_node=Spec.get_address(component, Names.NODES, Names.GROUP),
            ),
            SynthSpec(
                add_action=AddAction.ADD_AFTER,
                component=component,
                context=context,
                kwargs={
                    "active": Spec.get_address(
                        component, Names.CONTROL_BUSSES, Names.ACTIVE
                    ),
                    "in_": Spec.get_address(component, Names.AUDIO_BUSSES, Names.MAIN),
                    "out": Spec.get_address(
                        component, Names.CONTROL_BUSSES, Names.INPUT_LEVELS
                    ),
                },
                name=Names.INPUT_LEVELS,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, meters_synthdef.effective_name
                ),
                target_node=Spec.get_address(component, Names.NODES, Names.TRACKS),
            ),
            SynthSpec(
                add_action=AddAction.ADD_AFTER,
                component=component,
                context=context,
                kwargs={
                    "active": Spec.get_address(
                        component, Names.CONTROL_BUSSES, Names.ACTIVE
                    ),
                    "in_": Spec.get_address(component, Names.AUDIO_BUSSES, Names.MAIN),
                    "out": Spec.get_address(
                        component, Names.CONTROL_BUSSES, Names.OUTPUT_LEVELS
                    ),
                },
                name=Names.OUTPUT_LEVELS,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, meters_synthdef.effective_name
                ),
                target_node=Spec.get_address(
                    component, Names.NODES, Names.CHANNEL_STRIP
                ),
            ),
        ]
        if component.output is DEFAULT:
            output_patch_cable_synthdef = build_patch_cable(
                self.channel_count,
                component.parent.effective_channel_count,
            )
            specs.extend(
                [
                    SynthDefSpec(
                        component=component,
                        context=context,
                        name=output_patch_cable_synthdef.effective_name,
                        synthdef=output_patch_cable_synthdef,
                    ),
                    SynthSpec(
                        add_action=AddAction.ADD_TO_TAIL,
                        component=component,
                        context=context,
                        name=Names.OUTPUT,
                        kwargs={
                            "active": Spec.get_address(
                                component, Names.CONTROL_BUSSES, Names.ACTIVE
                            ),
                            "in_": Spec.get_address(component, Names.AUDIO_BUSSES, Names.MAIN),
                            "out": Spec.get_address(
                                component.parent, Names.AUDIO_BUSSES, Names.MAIN
                            ),
                        },
                        synthdef=Spec.get_address(
                            None, Names.SYNTHDEFS, output_patch_cable_synthdef.effective_name
                        ),
                        target_node=Spec.get_address(component, Names.NODES, Names.GROUP),
                    ),
                ]
            )
        return specs


class Track(TrackContainer[TrackContainer]):

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: TrackContainer | None = None,
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)
        TrackContainer.__init__(self)
        self._input: BusGroup | Track | None = None
        self._output: BusGroup | Default | TrackContainer | None = DEFAULT

    def _disconnect_parentage(self) -> None:
        if (parent := self._parent) is not None and self in parent._tracks:
            parent._tracks.remove(self)
        super()._disconnect_parentage()

    def _move(self, *, parent: TrackContainer, index: int) -> None:
        raise NotImplementedError

    def _resolve_initial_state(self) -> TrackState:
        return TrackState()

    def _resolve_state(self, context: AsyncServer | None = None) -> TrackState:
        return TrackState(
            channel_count=self.effective_channel_count,
        )

    async def add_send(self, target: "Track") -> None:
        async with self._lock:
            pass

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            self._delete()
            await self._reconcile(context=None)

    async def set_input(self, input_: Union[BusGroup, "Track"] | None) -> None:
        async with self._lock:
            self._input = input_
            await self._reconcile(context=self.context)

    async def set_output(
        self, output: Union[BusGroup, Default, "Track"] | None
    ) -> None:
        async with self._lock:
            self._output = output
            await self._reconcile(context=self.context)

    def set_name(self, name: str | None = None) -> None:
        self._name = name

    @property
    def address(self) -> Address:
        if self.parent is None:
            return "tracks[?]"
        index = self.parent.tracks.index(self)
        return f"{self.parent.address}.tracks[{index}]"

    @property
    def children(self) -> list[Component]:
        return [*self._tracks]

    @property
    def input(self) -> Union[BusGroup, "Track"] | None:
        return self._input

    @property
    def numeric_address(self) -> Address:
        return f"tracks[{self._id}]"

    @property
    def output(self) -> Union[BusGroup, Default, "Track"] | None:
        return self._output
