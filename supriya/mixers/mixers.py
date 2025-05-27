from typing import TYPE_CHECKING, Optional

from ..contexts import AsyncServer
from ..enums import AddAction, CalculationRate
from .components import (
    Component,
)
from .constants import Address, Names
from .specs import (
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


class Mixer(
    TrackContainer["Session"],
):
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

    def _delete(self) -> None:
        self._disconnect_parentage()

    def _disconnect_parentage(self) -> None:
        if (session := self._parent) is not None and self in (
            mixers := session._contexts.get(session._mixers.pop(self), [])
        ):
            mixers.remove(self)
        super()._disconnect_parentage()

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        if not context:
            return []
        if not self.parent:
            raise RuntimeError
        channel_strip_synthdef = build_channel_strip(self.effective_channel_count)
        meters_synthdef = build_meters(self.effective_channel_count)
        patch_cable_synthdef = build_patch_cable(
            self.effective_channel_count, self.effective_channel_count
        )
        return [
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
            SynthDefSpec(
                component=self,
                context=context,
                name=patch_cable_synthdef.effective_name,
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
                channel_count=1,
                component=self,
                context=context,
                name=Names.GAIN,
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
                name=Names.GROUP,
                target_node=None,
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
            SynthSpec(
                add_action=AddAction.ADD_TO_TAIL,
                component=self,
                context=context,
                kwargs={
                    "in_": Spec.get_address(self, Names.AUDIO_BUSSES, Names.MAIN),
                    "out": context.audio_output_bus_group,
                },
                name=Names.OUTPUT,
                synthdef=Spec.get_address(
                    None, Names.SYNTHDEFS, patch_cable_synthdef.effective_name
                ),
                target_node=Spec.get_address(self, Names.NODES, Names.GROUP),
            ),
        ]

    async def delete(self) -> None:
        # TODO: What are delete semantics actually?
        async with self._lock:
            await self._reconcile(context=None, deleting=True)

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
