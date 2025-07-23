from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer
from ..enums import AddAction, CalculationRate, DoneAction
from ..typing import Default
from ..ugens.system import (
    build_channel_strip_synthdef,
    build_meters_synthdef,
    build_patch_cable_synthdef,
)
from .components import (
    Component,
)
from .constants import Address, ChannelCount, Names
from .devices import DeviceContainer
from .specs import (
    BusSpec,
    GroupSpec,
    Spec,
    SynthDefSpec,
    SynthSpec,
)
from .tracks import TrackContainer

if TYPE_CHECKING:
    from .sessions import Session


class Mixer(
    DeviceContainer["Session"],
    TrackContainer,
):
    """
    A mixer component.

    Provides a container for devices and tracks running on a single synthesis
    context, although multiple mixers can run on the same context.
    """

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: Optional["Session"],
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)
        DeviceContainer.__init__(self)
        TrackContainer.__init__(self)
        self._add_parameter(name=Names.GAIN)

    def _delete(self) -> None:
        self._disconnect_parentage()

    def _disconnect_parentage(self) -> None:
        if (session := self._parent) is not None and self in (
            mixers := session._contexts.get(session._mixers.pop(self), [])
        ):
            mixers.remove(self)
        super()._disconnect_parentage()

    def _get_nested_address(self) -> Address:
        if self.session is None:
            return "mixers[?]"
        index = self.session.mixers.index(self)
        return f"session.mixers[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"mixers[{self._id}]"

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not context:
            return []
        specs = [
            SynthDefSpec(
                component=self,
                context=context,
                name=(
                    channel_strip_synthdef := build_channel_strip_synthdef(
                        self.effective_channel_count
                    )
                ).effective_name,
                synthdef=channel_strip_synthdef,
            ),
            SynthDefSpec(
                component=self,
                context=context,
                name=(
                    meters_synthdef := build_meters_synthdef(
                        self.effective_channel_count
                    )
                ).effective_name,
                synthdef=meters_synthdef,
            ),
            SynthDefSpec(
                component=self,
                context=context,
                name=(
                    patch_cable_synthdef := build_patch_cable_synthdef(
                        self.effective_channel_count,
                        min(
                            [
                                self.effective_channel_count,
                                len(context.audio_output_bus_group),
                            ]
                        ),
                    )
                ).effective_name,
                synthdef=patch_cable_synthdef,
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
                channel_count=self.effective_channel_count,
                component=self,
                context=context,
                name=Names.INPUT_LEVELS,
            ),
            BusSpec(
                calculation_rate=CalculationRate.CONTROL,
                channel_count=self.effective_channel_count,
                component=self,
                context=context,
                name=Names.OUTPUT_LEVELS,
            ),
            GroupSpec(
                add_action=AddAction.ADD_TO_HEAD,
                component=self,
                context=context,
                destroy_strategy={"gate": 0},
                name=Names.GROUP,
                parent_node=None,
                target_node=None,
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
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                destroy_strategy={
                    "done_action": DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                },
                kwargs={
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
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                kwargs={
                    "in_": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                    "out": context.audio_output_bus_group,
                },
                name=Names.OUTPUT,
                parent_node=None,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, patch_cable_synthdef.effective_name
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
        ]
        for parameter in self.parameters.values():
            specs.extend(parameter._resolve_specs(context=context))
        return specs

    async def delete(self) -> None:
        """
        Delete the mixer.
        """
        async with (session := self._ensure_session())._lock:
            await Component._reconcile(
                context=None,
                deleting_components=[self],
                reconciling_components=[self],
                session=session,
            )

    async def set_channel_count(self, channel_count: ChannelCount | Default) -> None:
        """
        Set the mixer's channel count.
        """
        async with (session := self._ensure_session())._lock:
            self._channel_count = channel_count
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    def set_name(self, name: str | None = None) -> None:
        """
        Set the mixer's name.
        """
        self._name = name

    @property
    def children(self) -> list[Component]:
        """
        Get the mixer's child components.
        """
        return [*self._tracks, *self._devices]

    @property
    def context(self) -> AsyncServer | None:
        """
        Get the component's ``Context``, if any.
        """
        if self.parent is None:
            return None
        return self.parent._mixers[self]

    @property
    def input_levels(self) -> list[float]:
        """
        Get the mixers's current input levels.

        Read from server shared memory.
        """
        # TODO: Test this.
        if not (shared_memory := self._ensure_context()._shared_memory):
            raise RuntimeError
        return shared_memory[self._artifacts.control_buses[Names.INPUT_LEVELS]]

    @property
    def output_levels(self) -> list[float]:
        """
        Get the mixers's current output levels.

        Read from server shared memory.
        """
        # TODO: Test this.
        if not (shared_memory := self._ensure_context()._shared_memory):
            raise RuntimeError
        return shared_memory[self._artifacts.control_buses[Names.OUTPUT_LEVELS]]
