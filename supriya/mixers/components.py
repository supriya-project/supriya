import asyncio
import dataclasses
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

from ..contexts import AsyncServer, Buffer, BusGroup, Context, Group, Node
from ..contexts.responses import QueryTreeGroup
from ..enums import AddAction, BootStatus, CalculationRate
from ..typing import DEFAULT, Default
from ..ugens import SynthDef
from ..utils import iterate_nwise

if TYPE_CHECKING:
    from .mixers import Mixer
    from .sessions import Session


@dataclasses.dataclass
class State:
    pass


ChannelCount: TypeAlias = Literal[1, 2, 4, 8]
Address: TypeAlias = str


@dataclasses.dataclass
class Spec:
    address: Address
    context: Context | None


@dataclasses.dataclass
class BufferSpec(Spec):
    channel_count: int
    count: int


@dataclasses.dataclass
class BusSpec(Spec):
    calculation_rate: CalculationRate
    count: int


@dataclasses.dataclass
class SynthDefSpec(Spec):
    synthdef: SynthDef


@dataclasses.dataclass
class NodeSpec(Spec):
    add_action: AddAction
    target_node: Address | None


@dataclasses.dataclass
class GroupSpec(NodeSpec):
    pass


@dataclasses.dataclass
class SynthSpec(NodeSpec):
    kwargs: dict[str, Address | float]
    synthdef: Address


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


class Component:

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent=None,
    ) -> None:
        self._audio_buses: dict[str, BusGroup] = {}
        self._buffers: dict[str, Buffer] = {}
        self._channel_count: ChannelCount | Default = DEFAULT
        self._control_buses: dict[str, BusGroup] = {}
        self._dependents: set[Component] = set()
        self._feedback_dependents: set[Component] = set()
        self._id = id_
        self._is_active = True
        self._lock = asyncio.Lock()
        self._name: str | None = name
        self._nodes: dict[str, Node] = {}
        self._parent = parent

    def __repr__(self) -> str:
        if self._name:
            return f"<{type(self).__name__} {self._id} {self._name!r} {self.address}>"
        return f"<{type(self).__name__} {self._id} {self.address}>"

    def _can_allocate(self) -> AsyncServer | None:
        if (
            context := self.context
        ) is not None and context.boot_status == BootStatus.ONLINE:
            return context
        return None

    def _disconnect_parentage(self) -> None:
        self._parent = None

    def _dump_components(self) -> list[str]:
        indent = "    "
        parts: list[str] = [repr(self)]
        for child in self.children:
            parts.extend(indent + line for line in child._dump_components())
        return parts

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    def _reconcile(self, context: AsyncServer | None = None) -> bool:
        return True

    def _resolve_initial_state(self) -> State:
        raise NotImplementedError

    def _resolve_spec_state(self, state: State) -> dict[Address, Spec | None]:
        raise NotImplementedError

    def _resolve_state(self, context: AsyncServer | None = None) -> State:
        raise NotImplementedError

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
    def address(self) -> Address:
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
    def numeric_address(self) -> Address:
        raise NotImplementedError

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
