import dataclasses
from typing import TYPE_CHECKING, Callable, Optional, Type

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction, CalculationRate, DoneAction
from ..typing import Default
from ..ugens import SynthDef
from ..ugens.system import build_patch_cable_synthdef
from .components import C, Component
from .constants import IO, Address, ChannelCount, Names
from .parameters import Field
from .specs import BusSpec, Spec, SynthDefSpec, SynthSpec

if TYPE_CHECKING:
    from .chains import Chain, Rack
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
    channel_count: Default | ChannelCount
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


class DeviceContainer(Component[C]):
    """
    A container for device components.

    Supports adding devices and grouping them.
    """

    def __init__(self) -> None:
        self._devices: list[Device] = []

    # TODO: add_instrument(
    #           voice_synthdefs: ...,
    #           effect_synthdefs: ...,
    #           parameters: ...,
    #           mappings: ...,
    #           sidechains: ...,
    #           polyphony: ...,
    #       ) -> Instrument:

    # TODO: group_devices(self, index: int, count: int, name: str | None = None) -> Rack

    def _add_device(
        self,
        *,
        device_class: Type["Device"] | None = None,
        name: str | None = None,
        parameter_configs: list[ParameterConfig] | None = None,
        sidechain_configs: list[SidechainConfig] | None = None,
        synth_configs: list[SynthConfig] | None = None,
    ) -> "Device":
        self._devices.append(
            device := (device_class or Device)(
                id_=self._ensure_session()._get_next_id(),
                name=name,
                parameter_configs=parameter_configs,
                parent=self,
                sidechain_configs=sidechain_configs,
                synth_configs=synth_configs,
            )
        )
        return device

    def _add_rack(self, *, name: str | None = None) -> tuple["Rack", "Chain"]:
        from .chains import Chain, Rack

        self._devices.append(
            rack := Rack(
                id_=self._ensure_session()._get_next_id(),
                name=name,
                parent=self,
            )
        )
        rack._chains.append(
            chain := Chain(
                id_=self._ensure_session()._get_next_id(),
                parent=rack,
            )
        )
        return rack, chain

    async def add_device(
        self,
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

    async def add_rack(self, *, name: str | None = None) -> "Rack":
        async with (session := self._ensure_session())._lock:
            rack, _ = self._add_rack(name=name)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[rack],
                session=session,
            )
            return rack

    @property
    def devices(self) -> list["Device"]:
        """
        Get the device container's devices.
        """
        return self._devices[:]


class Sidechain:
    def __init__(
        self,
        *,
        channel_count: Default | ChannelCount,
        component: Component,
        conditional: Callable[[], bool] | None = None,
        name: str,
    ) -> None:
        self._cached_input: Track | None = None
        self._channel_count = channel_count
        self._component = component
        self._conditional = conditional
        self._input: Track | None = None
        self._name = name

    def _notify_disconnected(self, connection: "Component") -> None:
        if connection is self._input:
            self.set(None)

    def _reconcile_connections(self, *, deleting: bool = False) -> list[Component]:
        related: list[Component] = []
        old_input = self._cached_input
        if deleting:
            if self._cached_input:
                self._cached_input._connections.pop((self.component, Names.INPUT), None)
                related.append(self._cached_input)
        else:
            new_input: Component | None = None
            if isinstance(self._input, Track):
                new_input = self._cached_input = self._input
            if old_input != new_input:
                if old_input:
                    old_input._connections.pop((self.component, Names.INPUT))
                if new_input:
                    new_input._connections[(self.component, Names.INPUT)] = IO.READ
            if old_input is not None:
                related.append(old_input)
            if new_input is not None:
                related.append(new_input)
        return related

    def _resolve_specs(
        self, context: AsyncServer | None, **parameters: float
    ) -> list[Spec]:
        if context is None:
            return []
        effective_channel_count = self.component.effective_channel_count
        # add the audio bus spec
        specs: list[Spec] = [
            BusSpec(
                calculation_rate=CalculationRate.AUDIO,
                channel_count=(
                    effective_channel_count
                    if isinstance(self.channel_count, Default)
                    else self.channel_count
                ),
                component=self.component,
                context=context,
                name=self.name,
            ),
        ]
        # bail if we don't need a patch-cable spec
        if not self.input or self.conditional and not self.conditional(**parameters):
            return specs
        # add the patch-cable spec
        input_feedsback = bool(
            Spec.feedsback(
                writer_order=self.input.feedback_graph_order,
                reader_order=self.component.graph_order,
            )
        )
        input_patch_cable_synthdef = build_patch_cable_synthdef(
            effective_channel_count,
            self.input.effective_channel_count,
            feedback=input_feedsback,
        )
        specs.extend(
            [
                SynthDefSpec(
                    component=self.component,
                    context=context,
                    name=input_patch_cable_synthdef.effective_name,
                    synthdef=input_patch_cable_synthdef,
                ),
                SynthSpec(
                    add_action=AddAction.ADD_TO_HEAD,
                    component=self.component,
                    context=context,
                    # destroy_strategy={"done_action": DoneAction.FREE_SYNTH, "gate": 0},
                    name=self.name,
                    kwargs={
                        # "active": ...?
                        "in_": Spec.get_address(
                            self.input,
                            Names.AUDIO_BUSES,
                            Names.MAIN,
                        ),
                        "out": Spec.get_address(
                            self.component, Names.AUDIO_BUSES, self.name
                        ),
                    },
                    parent_node=None,
                    synthdef=Spec.get_address(
                        None,
                        Names.SYNTHDEFS,
                        input_patch_cable_synthdef.effective_name,
                    ),
                    target_node=Spec.get_address(
                        self.component, Names.NODES, Names.GROUP
                    ),
                ),
            ]
        )
        return specs

    def set(self, input: Optional["Track"]) -> None:
        self._input = input

    @property
    def channel_count(self) -> ChannelCount | Default:
        return self._channel_count

    @property
    def component(self) -> "Component":
        return self._component

    @property
    def conditional(self) -> Callable[[], bool] | None:
        return self._conditional

    @property
    def input(self) -> Optional["Track"]:
        return self._input

    @property
    def name(self) -> str:
        return self._name


class Device(Component[DeviceContainer]):
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
        Component.__init__(self, id_=id_, name=name, parent=parent)
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
        channel_count: ChannelCount | Default,
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

    def _disconnect_parentage(self) -> None:
        self._ensure_parent()._devices.remove(self)
        super()._disconnect_parentage()

    def _get_nested_address(self) -> Address:
        if self.parent is None:
            return "devices[?]"
        index = self.parent.devices.index(self)
        return f"{self.parent.address}.devices[{index}]"

    def _get_numeric_address(self) -> Address:
        return f"devices[{self._id}]"

    def _move(self, *, new_parent: DeviceContainer, index: int) -> None:
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

    def _notify_disconnected(self, connection: "Component") -> bool:
        for sidechain in self._sidechains.values():
            sidechain._notify_disconnected(connection)
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

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if context is None:
            return []
        parent = self._ensure_parent()
        effective_channel_count = self.effective_channel_count
        specs: list[Spec] = [
            self._resolve_container_spec(
                context=context,
                destroy_strategy={
                    "done_action": DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP,
                    "gate": 0,
                },
                parent=(parent := self._ensure_parent()),
                parent_container=parent.devices,
                parent_container_group_name=Names.DEVICES,
            )
        ]
        options: dict[str, float] = {}
        for parameter in self._parameters.values():
            if parameter.field.has_bus:
                specs.extend(parameter._resolve_specs(context))
            else:
                options[parameter.name] = parameter.value
        for sidechain in self._sidechains.values():
            specs.extend(sidechain._resolve_specs(context, **options))
        # n.b. ordering synths is tricky :thinking:
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
                    parent, Names.AUDIO_BUSES, Names.MAIN
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
                            self, Names.CONTROL_BUSES, name
                        )
                    elif rate == CalculationRate.AUDIO:
                        synth_parameters[key] = Spec.get_address(
                            self, Names.AUDIO_BUSES, name
                        )
                    else:
                        raise ValueError(rate)
            specs.extend(
                [
                    SynthDefSpec(
                        component=self,
                        context=context,
                        name=synthdef.effective_name,
                        synthdef=synthdef,
                    ),
                    SynthSpec(
                        add_action=AddAction.ADD_TO_TAIL,
                        component=self,
                        context=context,
                        kwargs=synth_parameters,
                        name=f"synth-{index}",
                        parent_node=None,
                        synthdef=Spec.get_address(
                            None,
                            Names.SYNTHDEFS,
                            synthdef.effective_name,
                        ),
                        target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
                    ),
                ]
            )
        return specs

    async def delete(self) -> None:
        """
        Delete the device.
        """
        async with (session := self._ensure_session())._lock:
            await Component._reconcile(
                context=None,
                deleting_components=[self],
                reconciling_components=[self],
                session=session,
            )

    async def move(self, parent: DeviceContainer, index: int) -> None:
        """
        Move the device to another device container and/or index in a device
        container.
        """
        async with (session := self._ensure_session())._lock:
            self._move(new_parent=parent, index=index)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    def set_name(self, name: str | None = None) -> None:
        """
        Set the devices's name.
        """
        self._name = name

    async def set_sidechain(self, name: str, input: Optional["Track"]) -> None:
        async with (session := self._ensure_session())._lock:
            self._sidechains[name].set(input)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )

    @property
    def input_levels(self) -> list[float]:
        """
        Get the device's current input levels.

        Read from server shared memory.
        """
        # TODO: Use the container's input levels if this is the first track,
        #       otherwise use it's own input levels
        raise NotImplementedError

    @property
    def output_levels(self) -> list[float]:
        """
        Get the devices's current output levels.

        Read from server shared memory.
        """
        # TODO: Use the container's output levels if this is the last track,
        #       otherwise use it's own output levels
        raise NotImplementedError
