import dataclasses
from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer
from ..enums import AddAction, CalculationRate
from .components import (
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
from .tracks import TrackContainer

if TYPE_CHECKING:
    from .sessions import Session


@dataclasses.dataclass
class MixerState(State):
    channel_count: ChannelCount = 2

    def resolve_specs(
        self, component: Component, context: AsyncServer | None
    ) -> list[Spec]:
        if not context:
            return []
        if not component.parent:
            raise RuntimeError
        channel_strip_synthdef = build_channel_strip(self.channel_count)
        meters_synthdef = build_meters(self.channel_count)
        patch_cable_synthdef = build_patch_cable(self.channel_count, self.channel_count)
        return [
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
            SynthDefSpec(
                component=component,
                context=context,
                name=patch_cable_synthdef.effective_name,
                synthdef=patch_cable_synthdef,
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
                name=Names.GAIN,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=self.channel_count,
                component=component,
                context=context,
                name=Names.INPUT_LEVELS,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=self.channel_count,
                component=component,
                context=context,
                name=Names.OUTPUT_LEVELS,
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_HEAD,
                component=component,
                context=context,
                name=Names.GROUP,
                target_node=None,
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
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=component,
                context=context,
                kwargs={
                    "in_": Spec.get_address(component, Names.AUDIO_BUSSES, Names.MAIN),
                    "out": context.audio_output_bus_group,
                },
                name=Names.OUTPUT,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, patch_cable_synthdef.effective_name
                ),
                target_node=Spec.get_address(component, Names.NODES, Names.GROUP),
            ),
        ]


class Mixer(
    TrackContainer["Session"],
):
    # TODO: add_device() -> Device
    # TODO: group_devices(index: int, count: int) -> Rack
    # TODO: set_channel_count(self, channel_count: ChannelCount) -> None
    # TODO: set_output(output: int) -> None

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: Optional["Session"],
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)
        # DeviceContainer.__init__(self)
        TrackContainer.__init__(self)

    #   def _allocate(self, context: AsyncServer) -> bool:
    #       if not super()._allocate(context=context):
    #           return False
    #       # self._audio_buses["main"] = context.add_bus_group(
    #       #     calculation_rate=CalculationRate.AUDIO,
    #       #     count=2,
    #       # )
    #       main_audio_bus = self._get_audio_bus(
    #           context, name=Names.MAIN, can_allocate=True
    #       )
    #       gain_control_bus = self._get_control_bus(
    #           context, name=Names.GAIN, can_allocate=True
    #       )
    #       input_levels_control_bus = self._get_control_bus(
    #           context,
    #           name=Names.INPUT_LEVELS,
    #           can_allocate=True,
    #           channel_count=2,
    #       )
    #       output_levels_control_bus = self._get_control_bus(
    #           context,
    #           name=Names.OUTPUT_LEVELS,
    #           can_allocate=True,
    #           channel_count=2,
    #       )
    #       target_node = context.default_group
    #       with context.at():
    #           gain_control_bus.set(0.0)
    #           input_levels_control_bus.set(0.0)
    #           output_levels_control_bus.set(0.0)
    #           self._nodes[Names.GROUP] = group = target_node.add_group(
    #               add_action=AddAction.ADD_TO_TAIL
    #           )
    #           self._nodes[Names.TRACKS] = tracks = group.add_group(
    #               add_action=AddAction.ADD_TO_HEAD
    #           )
    #           self._nodes[Names.DEVICES] = group.add_group(
    #               add_action=AddAction.ADD_TO_TAIL
    #           )
    #           self._nodes[Names.CHANNEL_STRIP] = channel_strip = group.add_synth(
    #               add_action=AddAction.ADD_TO_TAIL,
    #               bus=main_audio_bus,
    #               gain=gain_control_bus.map_symbol(),
    #               synthdef=build_channel_strip(2),
    #           )
    #           self._nodes[Names.INPUT_LEVELS] = tracks.add_synth(
    #               add_action=AddAction.ADD_AFTER,
    #               synthdef=build_meters(2),
    #               in_=self._audio_buses[Names.MAIN],
    #               out=input_levels_control_bus,
    #           )
    #           self._nodes[Names.OUTPUT_LEVELS] = channel_strip.add_synth(
    #               add_action=AddAction.ADD_AFTER,
    #               synthdef=build_meters(2),
    #               in_=self._audio_buses[Names.MAIN],
    #               out=output_levels_control_bus,
    #           )
    #       return True

    def _disconnect_parentage(self) -> None:
        if (session := self._parent) is not None and self in (
            mixers := session._contexts.get(session._mixers.pop(self), [])
        ):
            mixers.remove(self)
        super()._disconnect_parentage()

    def _resolve_initial_state(self) -> MixerState:
        return MixerState()

    def _resolve_state(self, context: AsyncServer | None = None) -> MixerState:
        return MixerState(
            channel_count=self.effective_channel_count,
        )

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            self._delete()
            await self._reconcile(context=None)

    def set_name(self, name: str | None = None) -> None:
        self._name = name

    @property
    def address(self) -> Address:
        if self.session is None:
            return "mixers[?]"
        index = self.session.mixers.index(self)
        return f"session.mixers[{index}]"

    @property
    def children(self) -> list[Component]:
        # return [*self._tracks, *self._devices]
        return [*self._tracks]

    @property
    def context(self) -> AsyncServer | None:
        if self.parent is None:
            return None
        return self.parent._mixers[self]

    @property
    def numeric_address(self) -> Address:
        return f"mixers[{self._id}]"
