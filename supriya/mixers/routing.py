import dataclasses
import enum
from typing import Generic, Optional, TypeAlias, TypeVar

from ..contexts import AsyncServer, BusGroup
from ..enums import AddAction
from ..typing import Default
from ..ugens import SynthDef
from .components import A, AllocatableComponent, ComponentNames
from .synthdefs import build_patch_cable

Connectable: TypeAlias = AllocatableComponent | BusGroup | Default


class DefaultBehavior(enum.Enum):
    PARENT = enum.auto()
    GRANDPARENT = enum.auto()


S = TypeVar("S", bound=Connectable)

T = TypeVar("T", bound=Connectable)


class Connection(AllocatableComponent[A], Generic[A, S, T]):

    @dataclasses.dataclass
    class State:
        feedsback: bool | None = None
        inverted: bool = False
        postfader: bool = True
        source_bus: BusGroup | None = None
        source_component: AllocatableComponent | None = None
        target_bus: BusGroup | None = None
        target_component: AllocatableComponent | None = None

    def __init__(
        self,
        *,
        name: str,
        source: S | None,
        target: T | None,
        gain: float = 0.0,
        inverted: bool = False,
        parent: A | None = None,
        postfader: bool = True,
        writing: bool = True,
    ) -> None:
        super().__init__(parent=parent)
        self._cached_state = self.State()
        self._name = name
        self._postfader = postfader
        self._gain = gain
        self._inverted = inverted
        self._source = source
        self._target = target
        self._writing = writing
        self._reconcile()

    def _allocate(self, *, context: AsyncServer) -> bool:
        if not super()._allocate(context=context):
            return False
        return self._reconcile(context=context)

    def _allocate_synth(
        self,
        *,
        context: AsyncServer,
        parent: AllocatableComponent,
        new_state: "Connection.State",
    ) -> None:
        self._nodes[ComponentNames.SYNTH] = parent._nodes[
            ComponentNames.GROUP
        ].add_synth(
            active=parent._control_buses[ComponentNames.ACTIVE].map_symbol(),
            add_action=AddAction.ADD_TO_TAIL,
            in_=new_state.source_bus,
            out=new_state.target_bus,
            synthdef=build_patch_cable(2, 2),
            multiplier=-1 if new_state.inverted else 1,
        )

    def _deallocate(self) -> None:
        # NOTE: Resetting dependencies and state guarantees that the component-
        #       and node-tree reallocates idempotently on session reboot. In
        #       practice, this doesn't matter, but it does ensure the test
        #       suite doesn't need to special case node or bus IDs.
        super()._deallocate()
        self._reconcile(context=self._can_allocate(), new_state=self.State())

    def _get_synthdefs(self) -> list[SynthDef]:
        return [build_patch_cable(2, 2, feedback=True), build_patch_cable(2, 2)]

    def _reconcile(
        self,
        context: AsyncServer | None = None,
        new_state: Optional["Connection.State"] = None,
    ) -> bool:
        new_state = new_state or self._resolve_state(context)
        self._reconcile_dependencies(new_state)
        self._reconcile_synth(context, new_state)
        self._cached_state = new_state
        return self._reconcile_deferment(new_state)

    def _reconcile_deferment(self, new_state: "Connection.State") -> bool:
        if (
            new_state.source_component
            and new_state.target_component
            and not (new_state.source_bus and new_state.target_bus)
        ):
            return False
        return True

    def _reconcile_dependencies(self, new_state: "Connection.State") -> None:
        for new_component, old_component in [
            (new_state.source_component, self._cached_state.source_component),
            (new_state.target_component, self._cached_state.target_component),
        ]:
            if new_component is not old_component:
                if old_component:
                    old_component._unregister_dependency(self)
                if new_component:
                    new_component._register_dependency(self)
        if new_state.target_component and not new_state.feedsback:
            new_state.target_component._unregister_feedback(self)

    def _reconcile_synth(
        self, context: AsyncServer | None, new_state: "Connection.State"
    ) -> None:
        if self.parent is None:
            return
        if context is None:
            return
        if new_state == self._cached_state and self._nodes.get(ComponentNames.SYNTH):
            return
        with context.at():
            # Free the existing synth (if it exists)
            if synth := self._nodes.pop(ComponentNames.SYNTH, None):
                synth.free()
            # Add a new synth (if source and target buses exist)
            if new_state.source_bus and new_state.target_bus:
                self._allocate_synth(
                    context=context, parent=self.parent, new_state=new_state
                )

    def _resolve_default_source(
        self, context: AsyncServer | None
    ) -> tuple[AllocatableComponent | None, BusGroup | None]:
        # return self.parent
        raise NotImplementedError

    def _resolve_default_target(
        self, context: AsyncServer | None
    ) -> tuple[AllocatableComponent | None, BusGroup | None]:
        # return self.parent and self.parent.parent
        raise NotImplementedError

    def _resolve_feedback(
        self,
        context: AsyncServer | None,
        source_component: AllocatableComponent | None,
        target_component: AllocatableComponent | None,
    ) -> tuple[bool | None, BusGroup | None]:
        feedsback, target_bus = None, None
        try:
            source_order = source_component.graph_order if source_component else None
            target_order = target_component.graph_order if target_component else None
            feedsback = self.feedsback(
                source_order, target_order, writing=self._writing
            )
        except Exception:
            pass
        if self._writing and feedsback and target_component:
            target_bus = target_component._register_feedback(context, self)
        return feedsback, target_bus

    def _resolve_source(
        self, context: AsyncServer | None
    ) -> tuple[AllocatableComponent | None, BusGroup | None]:
        # resolve source
        source_component, source_bus = None, None
        if isinstance(self._source, BusGroup):
            source_bus = self._source
        elif isinstance(self._source, AllocatableComponent):
            source_component = self._source
        elif isinstance(self._source, Default):
            source_component, source_bus = self._resolve_default_source(context)
        if source_component:
            source_bus = source_component._audio_buses.get(ComponentNames.MAIN)
        return source_component, source_bus

    def _resolve_state(self, context: AsyncServer | None = None) -> "Connection.State":
        source_component, source_bus = self._resolve_source(context)
        target_component, target_bus = self._resolve_target(context)
        feedsback, feedback_bus = self._resolve_feedback(
            context, source_component, target_component
        )
        return self.State(
            feedsback=feedsback,
            inverted=self._inverted,
            postfader=self._postfader,
            source_component=source_component,
            source_bus=source_bus,
            target_component=target_component,
            target_bus=feedback_bus or target_bus,
        )

    def _resolve_target(
        self, context: AsyncServer | None
    ) -> tuple[AllocatableComponent | None, BusGroup | None]:
        target_component, target_bus = None, None
        if isinstance(self._target, BusGroup):
            target_bus = self._target
        elif isinstance(self._target, AllocatableComponent):
            target_component = self._target
        elif isinstance(self._target, Default):
            target_component, target_bus = self._resolve_default_target(context)
        if target_component:
            target_bus = target_component._audio_buses.get(ComponentNames.MAIN)
        return target_component, target_bus

    def _set_gain(self, gain: float) -> None:
        self._gain = gain

    def _set_inverted(self, inverted: bool) -> None:
        self._inverted = inverted

    def _set_postfader(self, postfader: bool) -> None:
        self._postfader = postfader
        self._reconcile(context=self._can_allocate())

    def _set_source(self, source: S | None) -> None:
        if isinstance(source, AllocatableComponent) and self.mixer is not source.mixer:
            raise RuntimeError
        self._source = source
        self._reconcile(context=self._can_allocate())

    def _set_target(self, target: T | None) -> None:
        if isinstance(target, AllocatableComponent) and self.mixer is not target.mixer:
            raise RuntimeError
        self._target = target
        self._reconcile(context=self._can_allocate())

    @classmethod
    def feedsback(
        cls,
        source_order: tuple[int, ...] | None,
        target_order: tuple[int, ...] | None,
        writing: bool = True,
    ) -> bool | None:
        if source_order is None or target_order is None:
            return None
        length = min(len(target_order), len(source_order))
        # If source_order is shallower than target_order, source_order might contain target_order
        if len(source_order) < len(target_order):
            feedsback = target_order[:length] <= source_order
        # If target_order is shallower than source_order, target_order might contain source_order
        elif len(target_order) < len(source_order):
            feedsback = target_order < source_order[:length]
        # If orders are same depth, check difference strictly
        else:
            feedsback = target_order <= source_order
        return feedsback

    @property
    def address(self) -> str:
        if self.parent is None:
            return self._name
        return f"{self.parent.address}.{self._name}"
