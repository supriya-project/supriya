import dataclasses
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Callable,
    Literal,
    Mapping,
    Optional,
    Protocol,
    Type,
    cast,
)

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


class Conditional(Protocol):
    def __call__(self, **options: float) -> bool:
        raise NotImplementedError


class SynthDefCallable(Protocol):
    def __call__(
        self,
        channel_count: ChannelCount,
    ) -> SynthDef:
        raise NotImplementedError


class SynthDefExtendedCallable(Protocol):
    def __call__(
        self,
        channel_count: ChannelCount,
        options: dict[str, float],
        sidechains: dict[str, tuple[int, bool]],
    ) -> SynthDef | None:
        raise NotImplementedError


class ChannelCountCallable(Protocol):
    def __call__(
        self,
        effective_channel_count: ChannelCount,
        options: dict[str, float],
    ) -> ChannelCount:
        raise NotImplementedError


@dataclasses.dataclass
class SidechainConfig:
    channel_count: ChannelCount | Inherit | ChannelCountCallable
    conditional: Conditional | None = None


@dataclasses.dataclass
class ParameterConfig:
    field: Field
    has_bus: bool = True


@dataclasses.dataclass
class SynthConfig:
    synthdef: SynthDef | SynthDefCallable | SynthDefExtendedCallable
    controls: (
        dict[
            str,
            float
            | tuple[CalculationRate, str]
            | Callable[[], float | tuple[CalculationRate, str]],
        ]
        | None
    ) = None
    conditional: Conditional | None = None


@dataclasses.dataclass
class DeviceConfig:
    name: str | None = None
    device_class: Type["Device"] | None = None
    parameter_configs: dict[str, Field | ParameterConfig] | None = None
    sidechain_configs: dict[str, ChannelCount | Inherit | SidechainConfig] | None = None
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
        parameter_configs: dict[str, Field | ParameterConfig] | None = None,
        sidechain_configs: dict[str, ChannelCount | Inherit | SidechainConfig]
        | None = None,
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
        from .racks import Rack

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
        for i in range(chain_count):
            rack._add_chain()
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
        parameter_configs: dict[str, Field | ParameterConfig] | None = None,
        sidechain_configs: dict[str, ChannelCount | Inherit | SidechainConfig]
        | None = None,
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

    def _get_input_levels_bus_group(self) -> BusGroup:
        parent = self._ensure_parent()
        index = parent._devices.index(self)
        # if we're the first device, return parent's input levels
        if not index:
            return parent._local_artifacts.control_buses[Names.INPUT_LEVELS]
        # otherwise return parent's input levels
        return parent._devices[index - 1]._local_artifacts.control_buses[
            Names.OUTPUT_LEVELS
        ]

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "devices[?]"
        index = self.parent.devices.index(self)
        return f"{self.parent.address}.devices[{index}]"

    def _get_output_levels_bus_group(self) -> BusGroup:
        return self._local_artifacts.control_buses[Names.OUTPUT_LEVELS]

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
    ) -> tuple[set[Component], set[Component]]:
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
                related.add(old_previous_device)
            if new_previous_device:
                related.add(new_previous_device)
        self._cached_previous_device = new_previous_device
        return related, deleted


class Sidechain:
    def __init__(
        self,
        *,
        channel_count: Inherit | ChannelCount | ChannelCountCallable,
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
        self, spec_factory: SpecFactory, **options: float
    ) -> tuple[ChannelCount, bool]:
        effective_channel_count = self.component.effective_channel_count
        if callable(self.channel_count):
            channel_count = self.channel_count(effective_channel_count, options)
        elif isinstance(self.channel_count, Inherit):
            channel_count = effective_channel_count
        else:
            channel_count = self.channel_count
        spec_factory.add_audio_bus(channel_count=channel_count, name=self.name)
        if not self._input._source or (
            self.conditional and not self.conditional(**options)
        ):
            return channel_count, False
        self._input._resolve_specs(spec_factory, target_channel_count=channel_count)
        return channel_count, True

    def set(self, input: Optional["Track"]) -> None:
        self._input.set(input)

    @property
    def channel_count(self) -> ChannelCount | Inherit | ChannelCountCallable:
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
        initial_parameters: dict[str, float] | None = None,
        initial_sidechains: dict[str, "Track"] | None = None,
        name: str | None = None,
        parameter_configs: dict[str, Field | ParameterConfig] | None = None,
        parent: DeviceContainer | None = None,
        sidechain_configs: dict[str, ChannelCount | Inherit | SidechainConfig]
        | None = None,
        synth_configs: list[SynthConfig] | None = None,
    ) -> None:
        DeviceBase.__init__(self, id_=id_, name=name, parent=parent)
        # validate parameters
        for name, parameter_config in (parameter_configs or {}).items():
            if not isinstance(parameter_config, ParameterConfig):
                parameter_config = ParameterConfig(field=parameter_config)
            self._add_parameter(
                field=parameter_config.field,
                has_bus=parameter_config.has_bus,
                name=name,
            )
        # validate sidechains
        self._sidechains: dict[str, Sidechain] = {}
        for name, sidechain_config in (sidechain_configs or {}).items():
            if not isinstance(sidechain_config, SidechainConfig):
                sidechain_config = SidechainConfig(channel_count=sidechain_config)
            self._add_sidechain(
                channel_count=sidechain_config.channel_count,
                conditional=sidechain_config.conditional,
                name=name,
            )
        # validate synthdef configs
        self._synth_configs: list[SynthConfig] = list(synth_configs or ())
        # set initial parameters, if any
        for name, value in (initial_parameters or {}).items():
            self._parameters[name].set(value)
        # set initial sidechains, if any
        for name, source in (initial_sidechains or {}).items():
            self._sidechains[name].set(source)

    def _add_sidechain(
        self,
        *,
        name: str,
        channel_count: ChannelCount | Inherit | ChannelCountCallable,
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
    ) -> tuple[set[Component], set[Component]]:
        related, deleted = super()._reconcile_connections(
            deleting=deleting, roots=roots
        )
        # check each sidechain
        for sidechain in self._sidechains.values():
            related.update(sidechain._reconcile_connections(deleting=deleting))
        return related, deleted

    def _resolve_specs(self, spec_factory: SpecFactory) -> SpecFactory:
        # cache
        effective_channel_count = self.effective_channel_count
        parent = self._ensure_parent()
        main_bus_address = parent._get_main_bus_address()
        # for parameterizing
        options: dict[str, float] = {}
        sidechains: dict[str, tuple[int, bool]] = {}
        # parameters
        for parameter in self._parameters.values():
            if parameter.has_bus:
                parameter._resolve_specs(spec_factory)
            else:
                options[parameter.name] = parameter.value
        # groups
        container_group_address = spec_factory.add_container_group(
            destroy_strategy=dict(
                done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP,
                gate=0,
            ),
            parent=(parent := self._ensure_parent()),
            parent_container=parent.devices,
            parent_container_group_name=Names.DEVICES,
        )
        synth_group_address = spec_factory.add_group(
            add_action=AddAction.ADD_TO_HEAD,
            name=Names.SYNTHS,
            target_node=container_group_address,
        )
        # sidechains
        for sidechain in self._sidechains.values():
            sidechains[sidechain.name] = sidechain._resolve_specs(
                spec_factory, **options
            )
        # synths
        add_action = AddAction.ADD_TO_TAIL
        target_node_address = synth_group_address
        for index, synth_config in enumerate(self._synth_configs):
            if synth_config.conditional and not synth_config.conditional(**options):
                continue
            synthdef: SynthDef | None
            if isinstance(synth_config.synthdef, SynthDef):
                synthdef = synth_config.synthdef
            elif callable(synth_config.synthdef):
                try:
                    synthdef = cast(SynthDefCallable, synth_config.synthdef)(
                        effective_channel_count
                    )
                except TypeError:
                    synthdef = cast(SynthDefExtendedCallable, synth_config.synthdef)(
                        effective_channel_count, options, sidechains
                    )
            if synthdef is None:
                continue
            controls: dict[str, Address | BusGroup | float] = {}
            for key in ["bus", "in_", "out"]:
                if key not in synthdef.parameters:
                    continue
                controls[key] = main_bus_address
            for key, value in (synth_config.controls or {}).items():
                if key not in synthdef.parameters:
                    continue
                if isinstance(
                    value_ := value(**options) if callable(value) else value, float
                ):
                    controls[key] = value_
                else:
                    rate, name = value_
                    if rate == CalculationRate.CONTROL:
                        controls[key] = Spec.get_address(
                            self, Entities.CONTROL_BUSES, name
                        )
                    elif rate == CalculationRate.AUDIO:
                        controls[key] = Spec.get_address(
                            self, Entities.AUDIO_BUSES, name
                        )
                    else:
                        raise ValueError(rate)
            synthdef_address = spec_factory.add_synthdef(synthdef=synthdef)
            target_node_address = spec_factory.add_synth(
                add_action=add_action,
                kwargs=controls,
                name=f"synth-{index}",
                synthdef=synthdef_address,
                target_node=target_node_address,
            )
            add_action = AddAction.ADD_AFTER
        # meters
        levels_control_bus_address = spec_factory.add_control_bus(
            channel_count=effective_channel_count,
            default=0.0,
            name=Names.OUTPUT_LEVELS,
        )
        meters_synthdef_address = spec_factory.add_synthdef(
            synthdef=build_meters_synthdef(effective_channel_count)
        )
        spec_factory.add_synth(
            add_action=AddAction.ADD_TO_TAIL,
            kwargs=dict(
                in_=main_bus_address,
                out=levels_control_bus_address,
            ),
            name=Names.OUTPUT_LEVELS,
            synthdef=meters_synthdef_address,
            target_node=container_group_address,
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
