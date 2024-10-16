import enum
from typing import Optional, Tuple, TypeAlias, Union

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction
from ..typing import DEFAULT, Default
from .components import A, AllocatableComponent
from .synthdefs import PATCH_CABLE_2

Connectable: TypeAlias = Optional[Union[AllocatableComponent, BusGroup, Default]]


class DefaultBehavior(enum.Enum):
    PARENT = enum.auto()
    GRANDPARENT = enum.auto()


class Connection(AllocatableComponent[A]):
    # TODO: We probably do want subclasses for input / output / send
    #       Because the default resolution behavior
    #       And allocation logic are subtly different

    def __init__(
        self,
        *,
        name: str,
        parent: Optional[A] = None,
        source: Connectable = DEFAULT,
        target: Connectable = DEFAULT,
    ) -> None:
        super().__init__(parent=parent)
        self._name = name
        self._source = source
        self._target = target
        # Computed
        self._cached_source_bus: Optional[BusGroup] = None
        self._cached_source_component: Optional[AllocatableComponent] = None
        self._cached_target_bus: Optional[BusGroup] = None
        self._cached_target_component: Optional[AllocatableComponent] = None
        self._reconcile_client_side()

    def _allocate(self, *, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        with context.at():
            return self._reconcile_server_side()

    def _allocate_synth(
        self, parent: AllocatableComponent, source_bus: BusGroup, target_bus: BusGroup
    ) -> None:
        self._nodes["synth"] = parent._nodes["group"].add_synth(
            add_action=AddAction.ADD_TO_TAIL,
            in_=source_bus,
            out=target_bus,
            synthdef=PATCH_CABLE_2,
        )

    def _cache(
        self, new_source_bus: Optional[BusGroup], new_target_bus: Optional[BusGroup]
    ) -> None:
        self._cached_source_bus = new_source_bus
        self._cached_target_bus = new_target_bus

    def _reconcile(self) -> None:
        self._reconcile_client_side()
        self._reconcile_server_side()

    def _reconcile_server_side(self) -> bool:
        source, new_source_bus = self._resolve_source()
        target, new_target_bus = self._resolve_target()
        # Defer if source and target should exist but either of their buses don't yet
        if source and target and not (new_source_bus and new_target_bus):
            return False
        # If any buses changed...
        if self._should_reallocate(new_source_bus, new_target_bus):
            # Free the existing synth (if it exists)
            if synth := self._nodes.pop("synth", None):
                synth.free()
            # Add a new synth (if source and target buses exist)
            if self.parent and new_source_bus and new_target_bus:
                self._allocate_synth(self.parent, new_source_bus, new_target_bus)
        self._cache(new_source_bus, new_target_bus)
        return True

    def _reconcile_client_side(self):
        new_source_component, _ = self._resolve_source()
        new_target_component, _ = self._resolve_target()
        if new_source_component is not self._cached_source_component:
            if (
                self._cached_source_component
                and self in self._source_component._dependents
            ):
                self._cached_source_component._dependents.remove(self)
            self._cached_source_component = new_source_component
            if self._cached_source_component:
                self._cached_source_component._dependents.add(self)
        if new_target_component is not self._cached_target_component:
            if (
                self._cached_target_component
                and self in self._cached_target_component._dependents
            ):
                self._cached_target_component._dependents.remove(self)
            self._cached_target_component = new_target_component
            if self._cached_target_component:
                self._cached_target_component._dependents.add(self)

    def _resolve_default_source_component(self) -> Optional[AllocatableComponent]:
        # return self.parent
        raise NotImplementedError

    def _resolve_default_target_component(self) -> Optional[AllocatableComponent]:
        # return self.parent and self.parent.parent
        raise NotImplementedError

    def _resolve_source(
        self,
    ) -> Tuple[Optional[AllocatableComponent], Optional[BusGroup]]:
        if self._source is None:
            return None, None
        elif isinstance(self._source, BusGroup):
            return None, self._source
        elif isinstance(self._source, AllocatableComponent):
            return self._source, self._source._audio_buses.get("main")
        elif source := self._resolve_default_source_component():
            return source, source._audio_buses.get("main")
        return None, None

    def _resolve_target(
        self,
    ) -> Tuple[Optional[AllocatableComponent], Optional[BusGroup]]:
        if self._target is None:
            return None, None
        elif isinstance(self._target, BusGroup):
            return None, self._target
        elif isinstance(self._target, AllocatableComponent):
            return self._target, self._target._audio_buses.get("main")
        elif target := self._resolve_default_target_component():
            return target, target._audio_buses.get("main")
        return None, None

    def _set_source(self, source: Connectable) -> None:
        if isinstance(source, AllocatableComponent) and self.mixer is not source.mixer:
            raise RuntimeError
        self._source = source
        self._reconcile_client_side()
        if (context := self._can_allocate()) is not None:
            with context.at():
                self._reconcile_server_side()

    def _set_target(self, target: Connectable) -> None:
        if isinstance(target, AllocatableComponent) and self.mixer is not target.mixer:
            raise RuntimeError
        self._target = target
        self._reconcile_client_side()
        if (context := self._can_allocate()) is not None:
            with context.at():
                self._reconcile_server_side()

    def _should_reallocate(
        self, new_source_bus: Optional[BusGroup], new_target_bus: Optional[BusGroup]
    ) -> bool:
        return (
            new_source_bus != self._cached_source_bus
            or new_target_bus != self._cached_target_bus
        )

    @property
    def address(self) -> str:
        if self.parent is None:
            return self._name
        return f"{self.parent.address}.{self._name}"
