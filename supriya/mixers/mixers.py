import dataclasses
from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer
from ..enums import AddAction
from .components import Address, ChannelCount, Component, ComponentNames, Spec, State
from .synthdefs import (
    build_channel_strip,
    build_meters,
)

if TYPE_CHECKING:
    from .sessions import Session


@dataclasses.dataclass
class MixerState(State):
    channel_count: ChannelCount = 2


class Mixer(Component):
    # TODO: add_device() -> Device
    # TODO: group_devices(index: int, count: int) -> Rack
    # TODO: set_channel_count(self, channel_count: ChannelCount) -> None
    # TODO: set_output(output: int) -> None

    def __init__(
        self,
        *,
        name: str | None = None,
        parent: Optional["Session"],
        session: "Session",
    ) -> None:
        Component.__init__(self, name=name, parent=parent, session=session)
        # DeviceContainer.__init__(self)
        # TrackContainer.__init__(self)

    def _allocate(self, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        # self._audio_buses["main"] = context.add_bus_group(
        #     calculation_rate=CalculationRate.AUDIO,
        #     count=2,
        # )
        main_audio_bus = self._get_audio_bus(
            context, name=ComponentNames.MAIN, can_allocate=True
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
        target_node = context.default_group
        with context.at():
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
        if (session := self._parent) is not None and self in (
            mixers := session._contexts.get(session._mixers.pop(self), [])
        ):
            mixers.remove(self)
        super()._disconnect_parentage()

    def _resolve_initial_state(self) -> MixerState:
        return MixerState()

    def _resolve_spec_state(self, state: MixerState) -> dict[Address, Spec | None]:
        return {}

    def _resolve_state(self, context: AsyncServer | None = None) -> MixerState:
        return MixerState(
            channel_count=self.effective_channel_count,
        )

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            self._delete()

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
        return [*self._tracks, *self._devices, self._output]

    @property
    def context(self) -> AsyncServer | None:
        if self.parent is None:
            return None
        return self.parent._mixers[self]

    @property
    def numeric_address(self) -> Address:
        return f"mixers[{self._id}]"
