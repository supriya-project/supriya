import asyncio
import dataclasses
from contextlib import nullcontext
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Generator,
    Generic,
    Iterator,
    Literal,
    Optional,
    Type,
    TypeAlias,
    TypeVar,
    cast,
)

from ..contexts import AsyncServer, Buffer, BusGroup, Group, Node
from ..contexts.responses import QueryTreeGroup
from ..enums import BootStatus, CalculationRate, DoneAction
from ..typing import DEFAULT, Default
from ..ugens import SynthDef
from ..utils import iterate_nwise


@dataclasses.dataclass
class State:
    context: AsyncServer | None = None


C = TypeVar("C", bound="Component")
H = TypeVar("H", bound=State)

# TODO: Integrate this with channel logic
ChannelCount: TypeAlias = Literal[1, 2, 4, 8]

if TYPE_CHECKING:
    from .mixers import Mixer
    from .sessions import Session


class ComponentNames:
    ACTIVE = "active"
    CHANNEL_STRIP = "channel-strip"
    DEVICES = "devices"
    FEEDBACK = "feedback"
    GAIN = "gain"
    GROUP = "group"
    INPUT = "input"
    INPUT_LEVELS = "input-levels"
    MAIN = "main"
    OUTPUT = "output"
    OUTPUT_LEVELS = "output-levels"
    SYNTH = "synth"
    TRACKS = "tracks"


class Component(Generic[C, H]):

    def __init__(
        self,
        *,
        name: str | None = None,
        parent: C | None = None,
    ) -> None:
        self._audio_buses: dict[str, BusGroup] = {}
        self._buffers: dict[str, Buffer] = {}
        self._channel_count: ChannelCount | Default = DEFAULT
        self._control_buses: dict[str, BusGroup] = {}
        self._dependents: set[Component] = set()
        self._feedback_dependents: set[Component] = set()
        self._is_active = True
        self._lock = asyncio.Lock()
        self._name: str | None = name
        self._nodes: dict[str, Node] = {}
        self._parent: C | None = parent
        self._cached_state: H = self._resolve_empty_state()

    def __repr__(self) -> str:
        if self._name:
            return f"<{type(self).__name__} {self._name!r} {self.address}>"
        return f"<{type(self).__name__} {self.address}>"

    async def _allocate_deep(self, *, context: AsyncServer) -> None:
        if self.session is None:
            raise RuntimeError
        fifo: list[tuple[Component, int]] = []
        current_synthdefs = self.session._synthdefs[context]
        desired_synthdefs: set[SynthDef] = set()
        for component in self._walk():
            fifo.append((component, 0))
            desired_synthdefs.update(component._get_synthdefs())
        if required_synthdefs := sorted(
            desired_synthdefs - current_synthdefs, key=lambda x: x.effective_name
        ):
            for synthdef in required_synthdefs:
                context.add_synthdefs(synthdef)
            await context.sync()
            current_synthdefs.update(required_synthdefs)
        while fifo:
            component, attempts = fifo.pop(0)
            if attempts > 2:
                raise RuntimeError(component, attempts)
            if not component._allocate(context=context):
                fifo.append((component, attempts + 1))

    def _allocate(self, *, context: AsyncServer) -> bool:
        return True

    def _can_allocate(self) -> AsyncServer | None:
        if (
            context := self.context
        ) is not None and context.boot_status == BootStatus.ONLINE:
            return context
        return None

    def _deallocate(self) -> None:
        context_manager = (
            context.at()
            if (context := self._can_allocate()) is not None
            else nullcontext()
        )
        with context_manager:
            for key in tuple(self._audio_buses):
                self._audio_buses.pop(key).free()
            for key in tuple(self._control_buses):
                self._control_buses.pop(key).free()
            self._nodes.clear()
            for key in tuple(self._buffers):
                self._buffers.pop(key).free()

    def _deallocate_deep(self) -> None:
        self._deallocate_root()
        for component in self._walk():
            component._deallocate()

    def _deallocate_root(self) -> None:
        context_manager = (
            context.at()
            if (context := self._can_allocate()) is not None
            else nullcontext()
        )
        group_node = self._nodes.get(ComponentNames.GROUP)
        synth_node = self._nodes.get(ComponentNames.CHANNEL_STRIP) or self._nodes.get(
            ComponentNames.SYNTH
        )
        with context_manager:
            if group_node:
                group_node.set(gate=0)
            elif synth_node:
                synth_node.set(gate=0)
            if group_node and synth_node:
                synth_node.set(done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP)

    def _delete(self) -> None:
        self._deallocate_root()
        for component in self._walk():
            component._deallocate()
            component._disconnect_dependents(root=self)
        self._disconnect_parentage()

    def _disconnect_dependents(self, root: "Component") -> None:
        # Delete (or disconnect) out-of-tree dependencies
        for dependent in sorted(self._dependents, key=lambda x: x.graph_order):
            dependent._disconnect_dependency(root=root, dependency=self)

    def _disconnect_dependency(
        self, root: "Component", dependency: "Component"
    ) -> None:
        pass

    def _disconnect_parentage(self) -> None:
        self._parent = None

    def _dump_components(self) -> list[str]:
        indent = "    "
        parts: list[str] = [repr(self)]
        for child in self.children:
            parts.extend(indent + line for line in child._dump_components())
        return parts

    def _get_audio_bus(
        self,
        context: AsyncServer | None,
        name: str,
        can_allocate: bool = False,
        channel_count: int = 2,
    ) -> BusGroup:
        return self._get_buses(
            calculation_rate=CalculationRate.AUDIO,
            can_allocate=can_allocate,
            channel_count=channel_count,
            context=context,
            name=name,
        )

    def _get_buses(
        self,
        context: AsyncServer | None,
        name: str,
        *,
        calculation_rate: CalculationRate,
        can_allocate: bool = False,
        channel_count: int = 1,
    ) -> BusGroup:
        if calculation_rate == CalculationRate.CONTROL:
            buses = self._control_buses
        elif calculation_rate == CalculationRate.AUDIO:
            buses = self._audio_buses
        else:
            raise ValueError(calculation_rate)
        if (name not in buses) and can_allocate and context:
            buses[name] = context.add_bus_group(
                calculation_rate=calculation_rate,
                count=channel_count,
            )
        return buses[name]

    def _get_control_bus(
        self,
        context: AsyncServer | None,
        name: str,
        can_allocate: bool = False,
        channel_count: int = 1,
    ) -> BusGroup:
        return self._get_buses(
            calculation_rate=CalculationRate.CONTROL,
            can_allocate=can_allocate,
            channel_count=channel_count,
            context=context,
            name=name,
        )

    def _get_synthdefs(self) -> list[SynthDef]:
        return []

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    def _reconcile(self, context: AsyncServer | None = None) -> bool:
        return True

    def _register_dependency(self, dependent: "Component") -> None:
        self._dependents.add(dependent)

    def _register_feedback(
        self, context: AsyncServer | None, dependent: "Component"
    ) -> BusGroup | None:
        self._dependents.add(dependent)
        self._feedback_dependents.add(dependent)
        return None

    def _resolve_empty_state(self) -> H:
        return cast(H, State())

    def _resolve_state(self, context: AsyncServer | None = None) -> State:
        raise NotImplementedError

    def _unregister_dependency(self, dependent: "Component") -> bool:
        self._dependents.discard(dependent)
        return self._unregister_feedback(dependent)

    def _unregister_feedback(self, dependent: "Component") -> bool:
        had_feedback = bool(self._feedback_dependents)
        self._feedback_dependents.discard(dependent)
        return had_feedback and not self._feedback_dependents

    def _walk(
        self, component_class: Type["Component"] | None = None
    ) -> Generator["Component", None, None]:
        component_class_ = component_class or Component
        if isinstance(self, component_class_):
            yield self
        for child in self.children:
            yield from child._walk(component_class_)

    def dump_components(self) -> str:
        return "\n".join(self._dump_components())

    async def dump_tree(self, annotated: bool = True) -> str:
        if self.session and self.session.status != BootStatus.ONLINE:
            raise RuntimeError
        tree = await cast(
            Awaitable[QueryTreeGroup],
            cast(Group, self._nodes[ComponentNames.GROUP]).dump_tree(),
        )
        if annotated:
            annotations: dict[int, str] = {}
            for component in self._walk():
                address = component.address
                for name, node in component._nodes.items():
                    annotations[node.id_] = f"{address}:{name}"
            return str(tree.annotate(annotations))
        return str(tree)

    @property
    def address(self) -> str:
        raise NotImplementedError

    @property
    def channel_count(self) -> ChannelCount | Default:
        return self._channel_count

    @property
    def children(self) -> list["Component"]:
        return []

    @property
    def context(self) -> AsyncServer | None:
        if (mixer := self.mixer) is not None:
            return mixer.context
        return None

    @property
    def effective_channel_count(self) -> ChannelCount:
        for component in self._iterate_parentage():
            if isinstance(channel_count := component.channel_count, int):
                return channel_count
        return 2

    @property
    def graph_order(self) -> tuple[int, ...]:
        # TODO: Cache this
        graph_order = []
        for parent, child in iterate_nwise(reversed(list(self._iterate_parentage()))):
            graph_order.append(parent.children.index(child))
        return tuple(graph_order)

    @property
    def mixer(self) -> Optional["Mixer"]:
        # TODO: Cache this
        from .mixers import Mixer

        for component in self._iterate_parentage():
            if isinstance(component, Mixer):
                return component
        return None

    @property
    def parent(self) -> C | None:
        return self._parent

    @property
    def parentage(self) -> list["Component"]:
        # TODO: Cache this
        return list(self._iterate_parentage())

    @property
    def session(self) -> Optional["Session"]:
        # TODO: Cache this
        from .sessions import Session

        for component in self._iterate_parentage():
            if isinstance(component, Session):
                return component
        return None

    @property
    def short_address(self) -> str:
        address = self.address
        for from_, to_ in [
            ("session.", ""),
            ("tracks", "t"),
            ("devices", "d"),
            ("mixers", "m"),
        ]:
            address = address.replace(from_, to_)
        return address
