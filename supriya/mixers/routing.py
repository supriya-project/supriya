from typing import Optional, Tuple, Union

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction
from ..typing import DEFAULT, Default
from .components import AllocatableComponent
from .synthdefs import PATCH_CABLE_2


class Connection(AllocatableComponent[AllocatableComponent]):

    def __init__(
        self,
        *,
        parent: Optional[AllocatableComponent] = None,
        source: Optional[Union[Default, AllocatableComponent]] = DEFAULT,
        target: Optional[Union[Default, AllocatableComponent]] = DEFAULT,
    ) -> None:
        super().__init__(parent=parent)
        self._source = source
        self._target = target
        # Computed
        self._source_bus: Optional[BusGroup] = None
        self._source_component: Optional[AllocatableComponent] = None
        self._target_bus: Optional[BusGroup] = None
        self._target_component: Optional[AllocatableComponent] = None
        self._reconcile_dependencies()

    def _allocate(self, *, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        with context.at():
            return self._reconcile_buses()

    def _reconcile_buses(self) -> bool:
        source, new_source_bus = self._resolve_source()
        target, new_target_bus = self._resolve_target()
        if source is None or target is None:
            return True
        if new_source_bus is None or new_target_bus is None:
            return False
        if new_source_bus != self._source_bus or new_target_bus != self._target_bus:
            if synth := self._nodes.pop("synth", None):
                synth.free()
            if self.parent is not None:
                self._nodes["synth"] = self.parent._nodes["group"].add_synth(
                    add_action=AddAction.ADD_TO_TAIL,
                    in_=new_source_bus,
                    out=new_target_bus,
                    synthdef=PATCH_CABLE_2,
                )
        self._source_bus = new_source_bus
        self._target_bus = new_target_bus
        return True

    def _reconcile_dependencies(self):
        new_source_component = self._resolve_source_component()
        new_target_component = self._resolve_target_component()
        if new_source_component is not self._source_component:
            if self._source_component and self in self._source_component._dependencies:
                self._source_component._dependencies.remove(self)
            self._source_component = new_source_component
            if self._source_component:
                self._source_component._dependencies.add(self)
        if new_target_component is not self._target_component:
            if self._target_component and self in self._target_component._dependencies:
                self._target_component._dependencies.remove(self)
            self._target_component = new_target_component
            if self._target_component:
                self._target_component._dependencies.add(self)

    def _resolve_default_source_component(self) -> Optional[AllocatableComponent]:
        return self.parent

    def _resolve_default_target_component(self) -> Optional[AllocatableComponent]:
        if self.parent and self.parent.parent:
            return self.parent.parent
        return None

    def _resolve_source(
        self,
    ) -> Tuple[Optional[AllocatableComponent], Optional[BusGroup]]:
        if source := self._resolve_source_component():
            return source, source._audio_buses.get("main")
        return None, None

    def _resolve_target(
        self,
    ) -> Tuple[Optional[AllocatableComponent], Optional[BusGroup]]:
        if target := self._resolve_target_component():
            return target, target._audio_buses.get("main")
        return None, None

    def _resolve_source_component(self) -> Optional[AllocatableComponent]:
        if self._source is None or isinstance(self._source, AllocatableComponent):
            return self._source
        return self._resolve_default_source_component()

    def _resolve_target_component(self) -> Optional[AllocatableComponent]:
        if self._target is None or isinstance(self._target, AllocatableComponent):
            return self._target
        return self._resolve_default_target_component()

    async def set_source(
        self, source: Optional[Union[Default, AllocatableComponent]]
    ) -> None:
        async with self._lock:
            self._source = source
            self._reconcile_dependencies()
            if context := self._can_allocate():
                with context.at():
                    self._reconcile_buses()

    async def set_target(
        self, target: Optional[Union[Default, AllocatableComponent]]
    ) -> None:
        async with self._lock:
            self._target = target
            self._reconcile_dependencies()
            if context := self._can_allocate():
                with context.at():
                    self._reconcile_buses()
