from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer
from ..enums import AddAction, CalculationRate, DoneAction
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
    NameSettable,
)
from .constants import Address, Entities, Names
from .devices import DeviceContainer
from .parameters import FloatField
from .specs import (
    BusSpec,
    GroupSpec,
    Spec,
    SpecFactory,
    SynthDefSpec,
    SynthSpec,
)
from .tracks import TrackContainer

if TYPE_CHECKING:
    from .sessions import Session


class Mixer(
    DeviceContainer["Session"],
    TrackContainer,
    ChannelSettable,
    Deletable,
    LevelsCheckable,
    NameSettable,
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
        self._add_parameter(name=Names.GAIN, field=FloatField(has_bus=True))

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

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        for parameter in self.parameters.values():
            parameter._resolve_specs(spec_factory)
        spec_factory.synthdef_specs.extend(
            [
                SynthDefSpec(
                    component=self,
                    context=spec_factory.context,
                    name=(
                        channel_strip_synthdef := build_channel_strip_synthdef(
                            self.effective_channel_count
                        )
                    ).effective_name,
                    synthdef=channel_strip_synthdef,
                ),
                SynthDefSpec(
                    component=self,
                    context=spec_factory.context,
                    name=(
                        meters_synthdef := build_meters_synthdef(
                            self.effective_channel_count
                        )
                    ).effective_name,
                    synthdef=meters_synthdef,
                ),
                SynthDefSpec(
                    component=self,
                    context=spec_factory.context,
                    name=(
                        patch_cable_synthdef := build_patch_cable_synthdef(
                            self.effective_channel_count,
                            min(
                                [
                                    self.effective_channel_count,
                                    len(spec_factory.context.audio_output_bus_group),
                                ]
                            ),
                        )
                    ).effective_name,
                    synthdef=patch_cable_synthdef,
                ),
            ]
        )
        spec_factory.bus_specs.extend(
            [
                BusSpec(
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=spec_factory.context,
                    name=Names.MAIN,
                ),
                BusSpec(
                    calculation_rate=CalculationRate.CONTROL,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=spec_factory.context,
                    name=Names.INPUT_LEVELS,
                ),
                BusSpec(
                    calculation_rate=CalculationRate.CONTROL,
                    channel_count=self.effective_channel_count,
                    component=self,
                    context=spec_factory.context,
                    name=Names.OUTPUT_LEVELS,
                ),
            ]
        )
        spec_factory.group_specs.extend(
            [
                GroupSpec(
                    add_action=AddAction.ADD_TO_HEAD,
                    component=self,
                    context=spec_factory.context,
                    destroy_strategy={"gate": 0},
                    name=Names.GROUP,
                    parent_node=None,
                    target_node=None,
                ),
                GroupSpec(
                    add_action=AddAction.ADD_TO_HEAD,
                    component=self,
                    context=spec_factory.context,
                    name=Names.TRACKS,
                    parent_node=None,
                    target_node=Spec.get_address(self, Entities.NODES, Names.GROUP),
                ),
                GroupSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=spec_factory.context,
                    name=Names.DEVICES,
                    parent_node=None,
                    target_node=Spec.get_address(self, Entities.NODES, Names.GROUP),
                ),
            ]
        )
        spec_factory.synth_specs.extend(
            [
                SynthSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=spec_factory.context,
                    destroy_strategy={
                        "done_action": DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP
                    },
                    kwargs={
                        "gain": Spec.get_address(
                            self, Entities.CONTROL_BUSES, Names.GAIN
                        ),
                        "out": Spec.get_address(self, Entities.AUDIO_BUSES, Names.MAIN),
                    },
                    name=Names.CHANNEL_STRIP,
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None, Entities.SYNTHDEFS, channel_strip_synthdef.effective_name
                    ),
                    target_node=Spec.get_address(self, Entities.NODES, Names.GROUP),
                ),
                SynthSpec(
                    add_action=AddAction.ADD_AFTER,
                    component=self,
                    context=spec_factory.context,
                    kwargs={
                        "in_": Spec.get_address(self, Entities.AUDIO_BUSES, Names.MAIN),
                        "out": Spec.get_address(
                            self, Entities.CONTROL_BUSES, Names.INPUT_LEVELS
                        ),
                    },
                    name=Names.INPUT_LEVELS,
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None, Entities.SYNTHDEFS, meters_synthdef.effective_name
                    ),
                    target_node=Spec.get_address(self, Entities.NODES, Names.TRACKS),
                ),
                SynthSpec(
                    add_action=AddAction.ADD_AFTER,
                    component=self,
                    context=spec_factory.context,
                    kwargs={
                        "in_": Spec.get_address(self, Entities.AUDIO_BUSES, Names.MAIN),
                        "out": Spec.get_address(
                            self, Entities.CONTROL_BUSES, Names.OUTPUT_LEVELS
                        ),
                    },
                    name=Names.OUTPUT_LEVELS,
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None, Entities.SYNTHDEFS, meters_synthdef.effective_name
                    ),
                    target_node=Spec.get_address(
                        self, Entities.NODES, Names.CHANNEL_STRIP
                    ),
                ),
                SynthSpec(
                    add_action=AddAction.ADD_TO_TAIL,
                    component=self,
                    context=spec_factory.context,
                    kwargs={
                        "in_": Spec.get_address(self, Entities.AUDIO_BUSES, Names.MAIN),
                        "out": spec_factory.context.audio_output_bus_group,
                    },
                    name=Names.OUTPUT,
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None, Entities.SYNTHDEFS, patch_cable_synthdef.effective_name
                    ),
                    target_node=Spec.get_address(self, Entities.NODES, Names.GROUP),
                ),
            ]
        )
        return spec_factory

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
