from typing import Optional, Union

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction, CalculationRate
from ..typing import DEFAULT, Default
from .components import (
    C,
    Component,
)
from .constants import IO, Address, Names
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
            return track

    async def group(self, index: int, count: int) -> "Track":
        async with self._lock:
            return self._group(index=index, count=count)

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

    def _reconcile_dependents(self) -> list["Component"]:
        if self.parent is None:
            raise ValueError
        self.parent._dependencies[(self, Names.INPUT)] = IO.READ
        self.target._dependencies[(self, Names.OUTPUT)] = IO.WRITE
        return sorted(
            [self.parent, self.target],
            key=lambda x: x.graph_order,
        )

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not self.parent:
            raise RuntimeError
        if not context:
            return []
        feedsback = bool(
            Spec.feedsback(
                source_order=self.graph_order,
                target_order=self.target.graph_order,
                writing=True,
            )
        )
        patch_cable_synthdef = build_patch_cable(
            self.parent.effective_channel_count,
            self.target.effective_channel_count,
            feedback=feedsback,
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
        self._cached_input: Track | None = None
        self._cached_output: TrackContainer | None = None
        self._input: BusGroup | Track | None = None
        self._output: BusGroup | Default | TrackContainer | None = DEFAULT
        self._sends: list[TrackSend] = []

    def _add_send(
        self,
        *,
        postfader: bool = True,
        target: TrackContainer,
    ) -> TrackSend:
        if (session := self.session) is None:
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

    def _delete(self) -> None:
        self._disconnect_parentage()

    def _disconnect_parentage(self) -> None:
        if (parent := self._parent) is not None and self in parent._tracks:
            parent._tracks.remove(self)
        super()._disconnect_parentage()

    def _move(self, *, parent: TrackContainer, index: int) -> None:
        raise NotImplementedError

    def _reconcile_dependents(self) -> list["Component"]:
        old_input = self._cached_input
        old_output = self._cached_output
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
                old_input._dependencies.pop((self, Names.INPUT))
            if new_input:
                new_input._dependencies[(self, Names.INPUT)] = IO.READ
        if old_output != new_output:
            if old_output:
                old_output._dependencies.pop((self, Names.OUTPUT))
            if new_output:
                new_output._dependencies[(self, Names.OUTPUT)] = IO.WRITE
        return sorted(
            [
                x
                for x in set([old_input, old_output, new_input, new_output])
                if x is not None
            ],
            key=lambda x: x.graph_order,
        )

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not context:
            return []
        if not self.parent:
            raise RuntimeError
        channel_strip_synthdef = build_channel_strip(self.effective_channel_count)
        meters_synthdef = build_meters(self.effective_channel_count)
        specs: list[Spec] = [
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
            GroupSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                name=Names.GROUP,
                # TODO: Need more advanced logic here for positioning
                target_node=Spec.get_address(self.parent, Names.NODES, Names.TRACKS),
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
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
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
        if self.output is DEFAULT or isinstance(self.output, TrackContainer):
            output_target_component = (
                self.parent if self.output is DEFAULT else self.parent
            )
            output_feedsback = bool(
                Spec.feedsback(
                    source_order=self.graph_order,
                    target_order=output_target_component.graph_order,
                    writing=True,
                )
            )
            output_patch_cable_synthdef = build_patch_cable(
                self.effective_channel_count,
                output_target_component.effective_channel_count,
                feedback=output_feedsback,
            )
            specs.extend(
                [
                    SynthDefSpec(
                        component=self,
                        context=context,
                        name=output_patch_cable_synthdef.effective_name,
                        synthdef=output_patch_cable_synthdef,
                    ),
                    SynthSpec(
                        add_action=AddAction.ADD_TO_TAIL,
                        component=self,
                        context=context,
                        name=Names.OUTPUT,
                        kwargs={
                            "active": Spec.get_address(
                                self, Names.CONTROL_BUSSES, Names.ACTIVE
                            ),
                            "in_": Spec.get_address(
                                self, Names.AUDIO_BUSSES, Names.MAIN
                            ),
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
                    ),
                ]
            )
        elif isinstance(self.output, BusGroup):
            output_patch_cable_synthdef = build_patch_cable(
                self.effective_channel_count,
                len(self.output),
            )
            specs.extend(
                [
                    SynthDefSpec(
                        component=self,
                        context=context,
                        name=output_patch_cable_synthdef.effective_name,
                        synthdef=output_patch_cable_synthdef,
                    ),
                    SynthSpec(
                        add_action=AddAction.ADD_TO_TAIL,
                        component=self,
                        context=context,
                        name=Names.OUTPUT,
                        kwargs={
                            "active": Spec.get_address(
                                self, Names.CONTROL_BUSSES, Names.ACTIVE
                            ),
                            "in_": Spec.get_address(
                                self, Names.AUDIO_BUSSES, Names.MAIN
                            ),
                            "out": self.output,
                        },
                        synthdef=Spec.get_address(
                            None,
                            Names.SYNTHDEFS,
                            output_patch_cable_synthdef.effective_name,
                        ),
                        target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                    ),
                ]
            )
        return specs

    async def add_device(self) -> None:
        async with self._lock:
            pass

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
            return send

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            await self._reconcile(context=None, deleting=True)

    async def move(self, parent: TrackContainer, index: int) -> None:
        async with self._lock:
            pass

    async def set_input(self, input_: Union[BusGroup, "Track"] | None) -> None:
        async with self._lock:
            self._input = input_
            await self._reconcile(context=self.context)

    async def set_output(
        self, output: Union[BusGroup, Default, TrackContainer] | None
    ) -> None:
        async with self._lock:
            self._output = output
            await self._reconcile(context=self.context)

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
        return [*self._tracks, *self._sends]

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
