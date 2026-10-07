from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer
from ..enums import AddAction, DoneAction
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
    Spec,
    SpecFactory,
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
        self._add_parameter(
            field=FloatField(),
            has_bus=True,
            name=Names.GAIN,
        )

    def _disconnect_parentage(self) -> None:
        if (session := self._parent) is not None and self in (
            mixers := session._contexts.get(session._mixers.pop(self), [])
        ):
            mixers.remove(self)

    def _get_nested_address(self) -> Address:
        if self.session is None:
            return "mixers[?]"
        index = self.session.mixers.index(self)
        return f"session.mixers[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"mixers[{self._id}]"

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
        patch_cable_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_patch_cable_synthdef(
                effective_channel_count,
                min(
                    [
                        effective_channel_count,
                        len(spec_factory.context.audio_output_bus_group),
                    ]
                ),
            )
        )
        # audio_buses
        main_audio_bus_address = spec_factory.add_audio_bus(
            channel_count=effective_channel_count,
            name=Names.MAIN,
        )
        # control buses
        input_levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            name=Names.INPUT_LEVELS,
        )
        output_levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            name=Names.OUTPUT_LEVELS,
        )
        # groups
        container_group_address = spec_factory.add_group(
            add_action=AddAction.ADD_TO_HEAD,
            destroy_strategy=dict(gate=0),
            name=Names.GROUP,
            target_node=None,
        )
        tracks_group_address = spec_factory.add_group(
            add_action=AddAction.ADD_TO_HEAD,
            name=Names.TRACKS,
            target_node=container_group_address,
        )
        spec_factory.add_group(
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
                in_=main_audio_bus_address,
                out=output_levels_control_bus_address,
            ),
            name=Names.OUTPUT_LEVELS,
            synthdef=meters_synthdef_address,
            target_node=channel_strip_synth_address,
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_TO_TAIL,
            kwargs=dict(
                in_=main_audio_bus_address,
                out=spec_factory.context.audio_output_bus_group,
            ),
            name=Names.OUTPUT,
            synthdef=patch_cable_synthdef_address,
            target_node=container_group_address,
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
