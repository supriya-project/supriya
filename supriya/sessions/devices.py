import dataclasses
from types import MappingProxyType
from typing import TYPE_CHECKING, Callable, Literal, Mapping, Optional, Type

from ..contexts import BusGroup
from ..enums import AddAction, CalculationRate, DoneAction
from ..typing import Inherit
from ..ugens import SynthDef
from ..ugens.system import build_meters_synthdef
from .components import C, Component, Deletable, LevelsCheckable, Movable, NameSettable
from .constants import Address, ChannelCount, Entities, Names, PatchMode
from .parameters import Field
from .routing import Input
from .specs import Spec, SpecFactory

if TYPE_CHECKING:
    from .racks import Chain, Rack
    from .tracks import Track


# TODO: We need to differentiate the concept of control bus managing parameters
#       and just general option paramaters with no specific server
#       representation. And for both, we need concepts of unit, range, etc.


@dataclasses.dataclass
class ParameterConfig:
    name: str
    field: Field


@dataclasses.dataclass
class SidechainConfig:
    name: str
    channel_count: Inherit | ChannelCount
    conditional: Callable[[], bool] | None = None


@dataclasses.dataclass
class SynthConfig:
    synthdef: SynthDef | Callable[[ChannelCount], SynthDef | None]
    parameters: (
        dict[
            str,
            float
            | tuple[CalculationRate, str]
            | Callable[[], float | tuple[CalculationRate, str]],
        ]
        | None
    ) = None


@dataclasses.dataclass
class DeviceConfig:
    name: str | None = None
    device_class: Type["Device"] | None = None
    parameter_configs: list[ParameterConfig] | None = None
    sidechain_configs: list[SidechainConfig] | None = None
    synth_configs: list[SynthConfig] | None = None


class DeviceContainer(Component[C]):
    """
    A container for device components.

    Supports adding devices and grouping them.
    """

    def __init__(self) -> None:
        self._devices: list[DeviceBase] = []

    def _add_device(
        self,
        *,
        device_config: DeviceConfig | None = None,
        device_class: Type["Device"] | None = None,
        name: str | None = None,
        parameter_configs: list[ParameterConfig] | None = None,
        sidechain_configs: list[SidechainConfig] | None = None,
        synth_configs: list[SynthConfig] | None = None,
    ) -> "Device":
        device_config = device_config or DeviceConfig()
        self._devices.append(
            device := (device_class or device_config.device_class or Device)(
                id_=self._ensure_session()._get_next_id(),
                name=name or device_config.name,
                parameter_configs=parameter_configs or device_config.parameter_configs,
                parent=self,
                sidechain_configs=sidechain_configs or device_config.sidechain_configs,
                synth_configs=synth_configs or device_config.synth_configs,
            )
        )
        return device

    def _add_rack(
        self,
        *,
        chain_count: int = 1,
        name: str | None = None,
        read_mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE] = PatchMode.REPLACE,
        write_mode: PatchMode = PatchMode.SUM,
    ) -> tuple["Rack", Optional["Chain"]]:
        from .racks import Chain, Rack

        if chain_count < 0:
            raise ValueError(chain_count)
        self._devices.append(
            rack := Rack(
                id_=self._ensure_session()._get_next_id(),
                name=name,
                parent=self,
                read_mode=read_mode,
                write_mode=write_mode,
            )
        )
        for _ in range(chain_count):
            rack._chains.append(
                Chain(
                    id_=self._ensure_session()._get_next_id(),
                    parent=rack,
                )
            )
        return rack, rack._chains[0] if rack._chains else None

    def _get_main_bus_address(self) -> Address:
        return Spec.get_address(self, Entities.AUDIO_BUSES, Names.MAIN)

    def _group_devices(
        self,
        *,
        index: int,
        count: int,
        name: str | None = None,
        read_mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE] = PatchMode.REPLACE,
        write_mode: PatchMode = PatchMode.SUM,
    ) -> "Rack":
        if index < 0:
            raise RuntimeError(index)
        elif count < 1:
            raise RuntimeError(count)
        elif (index + count) > len(self.devices):
            raise RuntimeError(index, count)
        rack, chain = self._add_rack(
            name=name,
            read_mode=read_mode,
            write_mode=write_mode,
        )
        assert chain is not None
        child_devices = self._devices[index : index + count]
        chain._devices[:] = child_devices
        self._devices[index : index + count] = [rack]
        for device in child_devices:
            device._parent = chain
        return rack

    async def add_device(
        self,
        device_config: DeviceConfig | None = None,
        *,
        device_class: Type["Device"] | None = None,
        name: str | None = None,
        parameter_configs: list[ParameterConfig] | None = None,
        sidechain_configs: list[SidechainConfig] | None = None,
        synth_configs: list[SynthConfig] | None = None,
    ) -> "Device":
        """
        Add a new device to the device container.
        """
        async with (session := self._ensure_session())._lock:
            device = self._add_device(
                device_config=device_config,
                device_class=device_class,
                name=name,
                parameter_configs=parameter_configs,
                sidechain_configs=sidechain_configs,
                synth_configs=synth_configs,
            )
            await Component._reconcile(
                context=self.context,
                reconciling_components=[device],
                session=session,
            )
            return device

    async def add_rack(
        self,
        *,
        chain_count: int = 1,
        name: str | None = None,
        read_mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE] = PatchMode.REPLACE,
        write_mode: PatchMode = PatchMode.SUM,
    ) -> "Rack":
        async with (session := self._ensure_session())._lock:
            rack, _ = self._add_rack(
                chain_count=chain_count,
                name=name,
                read_mode=read_mode,
                write_mode=write_mode,
            )
            await Component._reconcile(
                context=self.context,
                reconciling_components=[rack],
                session=session,
            )
            return rack

    async def group_devices(
        self,
        index: int,
        count: int,
        *,
        name: str | None = None,
        read_mode: Literal[PatchMode.IGNORE, PatchMode.REPLACE] = PatchMode.REPLACE,
        write_mode: PatchMode = PatchMode.SUM,
    ) -> "Rack":
        """
        Group one or more devices in the devices container as children of a new rack.
        """
        async with (session := self._ensure_session())._lock:
            rack = self._group_devices(
                index=index,
                count=count,
                name=name,
                read_mode=read_mode,
                write_mode=write_mode,
            )
            await Component._reconcile(
                context=self.context,
                reconciling_components=[rack],
                session=session,
            )
            return rack

    @property
    def devices(self) -> list["DeviceBase"]:
        """
        Get the device container's devices.
        """
        return self._devices[:]


class DeviceBase(Deletable[DeviceContainer], LevelsCheckable, Movable, NameSettable):
    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: DeviceContainer | None = None,
    ) -> None:
        Component.__init__(self, id_=id_, name=name, parent=parent)
        self._cached_previous_device: DeviceBase | None = None

    def _disconnect_parentage(self) -> None:
        self._ensure_parent()._devices.remove(self)
        super()._disconnect_parentage()

    def _get_input_levels_bus_group(self) -> BusGroup:
        parent = self._ensure_parent()
        index = parent._devices.index(self)
        # if we're the first device, return parent's input levels
        if not index:
            return parent._artifacts.control_buses[Names.INPUT_LEVELS]
        # otherwise return parent's input levels
        return parent._devices[index - 1]._artifacts.control_buses[Names.LEVELS]

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "devices[?]"
        index = self.parent.devices.index(self)
        return f"{self.parent.address}.devices[{index}]"

    def _get_output_levels_bus_group(self) -> BusGroup:
        parent = self._ensure_parent()
        return (
            self._artifacts.control_buses.get(Names.LEVELS)
            or parent._artifacts.control_buses[Names.OUTPUT_LEVELS]
        )

    def _get_numeric_address(self) -> Address:
        return f"devices[{self._id}]"

    def _move(self, *, new_parent: DeviceContainer, index: int) -> None:
        # TODO: We /also/ need to reconcile the previous device in the old
        #       parent (if any) And the previous device in the new parent (if
        #       any) because per-device meters are position-dependent.
        #       Maybe this can be done on a connection level?
        # Validate if moving is possible
        if self.mixer is not new_parent.mixer:
            raise RuntimeError
        elif self in new_parent.parentage:
            raise RuntimeError
        elif index < 0:
            raise RuntimeError
        elif index and index >= len(new_parent.devices):
            raise RuntimeError
        # Reconfigure parentage and bail if this is a no-op
        old_parent = self._ensure_parent()
        old_index = old_parent._devices.index(self)
        if old_parent is new_parent and old_index == index:
            return  # Bail
        old_parent._devices.remove(self)
        self._parent = new_parent
        new_parent._devices.insert(index, self)

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: list[Component] | None = None,
    ) -> tuple[list[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(
            deleting=deleting, roots=roots
        )
        parent = self._ensure_parent()
        index = parent._devices.index(self)
        old_previous_device = self._cached_previous_device
        new_previous_device: DeviceBase | None = None
        if index:
            new_previous_device = parent._devices[index - 1]
        if old_previous_device is not new_previous_device:
            if old_previous_device:
                related.append(old_previous_device)
            if new_previous_device:
                related.append(new_previous_device)
        self._cached_previous_device = new_previous_device
        return sorted(set(related), key=lambda x: x.graph_order), deleted


class Sidechain:
    def __init__(
        self,
        *,
        channel_count: Inherit | ChannelCount,
        component: Component,
        conditional: Callable[[], bool] | None = None,
        name: str,
    ) -> None:
        self._channel_count = channel_count
        self._component = component
        self._conditional = conditional
        self._input = Input(
            add_action=AddAction.ADD_TO_HEAD,
            add_node_address=Spec.get_address(component, Entities.NODES, Names.GROUP),
            host_component=component,
            name=name,
            target_bus_address=Spec.get_address(
                component,
                Entities.AUDIO_BUSES,
                name,
            ),
        )
        self._name = name

    def _on_connection_deleted(self, connection: "Component") -> None:
        self._input._on_connection_deleted(connection)

    def _reconcile_connections(self, *, deleting: bool = False) -> list[Component]:
        return self._input._reconcile_connections(deleting=deleting)

    def _resolve_specs(
        self, spec_factory: SpecFactory, **parameters: float
    ) -> SpecFactory:
        effective_channel_count = self.component.effective_channel_count
        spec_factory.add_audio_bus(
            channel_count=(
                effective_channel_count
                if isinstance(self.channel_count, Inherit)
                else self.channel_count
            ),
            name=self.name,
        )
        if not self._input._source or (
            self.conditional and not self.conditional(**parameters)
        ):
            return spec_factory
        self._input._resolve_specs(spec_factory)
        return spec_factory

    def set(self, input: Optional["Track"]) -> None:
        self._input.set(input)

    @property
    def channel_count(self) -> ChannelCount | Inherit:
        return self._channel_count

    @property
    def component(self) -> "Component":
        return self._component

    @property
    def conditional(self) -> Callable[[], bool] | None:
        return self._conditional

    @property
    def name(self) -> str:
        return self._name

    @property
    def source(self) -> Optional["Track"]:
        from .tracks import Track

        if (source := self._input._source) is not None:
            assert isinstance(source, Track)
        return source


class Device(DeviceBase):
    """
    A device component.

    Base class for implementing control devices (e.g. MIDI manipulation), audio
    effects, and instruments.
    """

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: DeviceContainer | None = None,
        parameter_configs: list[ParameterConfig] | None = None,
        sidechain_configs: list[SidechainConfig] | None = None,
        synth_configs: list[SynthConfig] | None = None,
    ) -> None:
        DeviceBase.__init__(self, id_=id_, name=name, parent=parent)
        # validate parameters
        for parameter_config in parameter_configs or ():
            self._add_parameter(
                field=parameter_config.field,
                name=parameter_config.name,
            )
        # validate sidechains
        self._sidechains: dict[str, Sidechain] = {}
        for sidechain_config in sidechain_configs or ():
            self._add_sidechain(
                channel_count=sidechain_config.channel_count,
                conditional=sidechain_config.conditional,
                name=sidechain_config.name,
            )
        # validate synthdef configs
        self._synth_configs: list[SynthConfig] = list(synth_configs or ())

    def _add_sidechain(
        self,
        *,
        name: str,
        channel_count: ChannelCount | Inherit,
        conditional: Callable[[], bool] | None = None,
    ) -> Sidechain:
        if name in self._sidechains:
            raise ValueError(name)
        self._sidechains[name] = sidechain = Sidechain(
            channel_count=channel_count,
            component=self,
            name=name,
            conditional=conditional,
        )
        return sidechain

    def _on_connection_deleted(self, connection: "Component") -> bool:
        for sidechain in self._sidechains.values():
            sidechain._on_connection_deleted(connection)
        return False

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: list[Component] | None = None,
    ) -> tuple[list[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(
            deleting=deleting, roots=roots
        )
        # check each sidechain
        for sidechain in self._sidechains.values():
            related.extend(sidechain._reconcile_connections(deleting=deleting))
        return sorted(set(related), key=lambda x: x.graph_order), deleted

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        parent = self._ensure_parent()
        effective_channel_count = self.effective_channel_count
        container_group_address = spec_factory.add_container_group(
            destroy_strategy=dict(
                done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP,
                gate=0,
            ),
            parent=(parent := self._ensure_parent()),
            parent_container=parent.devices,
            parent_container_group_name=Names.DEVICES,
        )
        options: dict[str, float] = {}
        for parameter in self._parameters.values():
            if parameter.field.has_bus:
                parameter._resolve_specs(spec_factory)
            else:
                options[parameter.name] = parameter.value
        for sidechain in self._sidechains.values():
            sidechain._resolve_specs(spec_factory, **options)
        # n.b. ordering synths is tricky :thinking:.
        #      increasingly feels like we need a NodeOrderSpec.
        add_action = AddAction.ADD_TO_TAIL
        target_node_address = container_group_address
        for index, synth_config in enumerate(self._synth_configs):
            if (
                synthdef := (
                    synth_config.synthdef(effective_channel_count, **options)
                    if callable(synth_config.synthdef)
                    else synth_config.synthdef
                )
            ) is None:
                continue
            synth_parameters: dict[str, Address | BusGroup | float] = {}
            for key in ["bus", "in_", "out"]:
                if key not in synthdef.parameters:
                    continue
                synth_parameters[key] = Spec.get_address(
                    parent, Entities.AUDIO_BUSES, Names.MAIN
                )
            for key, value in (synth_config.parameters or {}).items():
                if key not in synthdef.parameters:
                    continue
                if isinstance(
                    value_ := value(**options) if callable(value) else value, float
                ):
                    synth_parameters[key] = value_
                else:
                    rate, name = value_
                    if rate == CalculationRate.CONTROL:
                        synth_parameters[key] = Spec.get_address(
                            self, Entities.CONTROL_BUSES, name
                        )
                    elif rate == CalculationRate.AUDIO:
                        synth_parameters[key] = Spec.get_address(
                            self, Entities.AUDIO_BUSES, name
                        )
                    else:
                        raise ValueError(rate)
            synthdef_address = spec_factory.add_synthdef(synthdef=synthdef)
            target_node_address = spec_factory.add_synth(
                add_action=add_action,
                kwargs=synth_parameters,
                name=f"synth-{index}",
                synthdef=synthdef_address,
                target_node=target_node_address,
            )
            add_action = AddAction.ADD_AFTER
        # meters
        if parent._devices.index(self) < (len(parent._devices) - 1):
            # will the meters synth follow the group on move?
            levels_control_bus_address = spec_factory.add_control_bus(
                channel_count=self.effective_channel_count,
                default=0.0,
                name=Names.LEVELS,
            )
            meters_synthdef_address = spec_factory.add_synthdef(
                synthdef=build_meters_synthdef(self.effective_channel_count)
            )
            spec_factory.add_synth(
                add_action=add_action,
                kwargs=dict(
                    in_=parent._get_main_bus_address(),
                    out=levels_control_bus_address,
                ),
                name=Names.LEVELS,
                synthdef=meters_synthdef_address,
                target_node=target_node_address,
            )
        return spec_factory

    async def set_sidechain(self, name: str, source: Optional["Track"]) -> None:
        async with (session := self._ensure_session())._lock:
            self._sidechains[name].set(source)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    @property
    def sidechains(self) -> Mapping[str, Sidechain]:
        return MappingProxyType(self._sidechains)
