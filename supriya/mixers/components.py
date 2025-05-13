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

from ..contexts import AsyncServer, Buffer, BusGroup, ContextObject, Group, Node
from ..contexts.responses import QueryTreeGroup
from ..enums import AddAction, BootStatus, CalculationRate
from ..typing import DEFAULT, Default
from ..ugens import SynthDef
from ..utils import iterate_nwise

C = TypeVar("C", bound="Component")

if TYPE_CHECKING:
    from .mixers import Mixer
    from .sessions import Session


@dataclasses.dataclass
class State:

    def resolve_specs(
        self, component: "Component", context: AsyncServer | None
    ) -> list["Spec"]:
        raise NotImplementedError


ChannelCount: TypeAlias = Literal[1, 2, 4, 8]
Address: TypeAlias = str


@dataclasses.dataclass
class Spec:
    address: Address
    context: AsyncServer

    def create(
        self,
        context: AsyncServer,
        old_artifacts: dict[Address, ContextObject],
        new_artifacts: dict[Address, ContextObject],
    ) -> None:
        raise NotImplementedError

    def destroy(
        self, context: AsyncServer, old_artifacts: dict[Address, ContextObject]
    ) -> None:
        raise NotImplementedError

    def mutate(
        self,
        context: AsyncServer,
        old_artifacts: dict[Address, ContextObject],
        new_artifacts: dict[Address, ContextObject],
    ) -> None:
        raise NotImplementedError

    def requires_recreation(self, other_spec: "Spec") -> bool:
        raise NotImplementedError


@dataclasses.dataclass
class BufferSpec(Spec):
    channel_count: int
    count: int


@dataclasses.dataclass
class BusSpec(Spec):
    calculation_rate: CalculationRate
    channel_count: int


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


class Names:
    ACTIVE = "active"
    AUDIO_BUSSES = "audio-busses"
    BUFFERS = "buffers"
    CHANNEL_STRIP = "channel-strip"
    CONTROL_BUSSES = "control-busses"
    DEVICES = "devices"
    FEEDBACK = "feedback"
    GAIN = "gain"
    GROUP = "group"
    INPUT = "input"
    INPUT_LEVELS = "input-levels"
    MAIN = "main"
    NODES = "nodes"
    OUTPUT = "output"
    OUTPUT_LEVELS = "output-levels"
    SYNTH = "synth"
    SYNTHDEFS = "synthdefs"
    TRACKS = "tracks"


class Component(Generic[C]):

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: C | None = None,
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
        self._parent: C | None = parent
        self._specs: list[Spec] = []
        self._state: State = self._resolve_initial_state()

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

    def _delete(self) -> None:
        pass

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

    async def _reconcile(self, context: AsyncServer | None = None) -> tuple[
        dict[AsyncServer, dict[Address, Spec]],
        dict[AsyncServer, dict[Address, tuple[Spec, Spec]]],
        dict[AsyncServer, dict[Address, Spec]],
    ]:
        if self.session is None:
            raise ValueError
        # Need access to remote state and remote state updates
        # Merge these together as changes are applied against the cluster
        # Deletes always happen against the old artifacts
        old_artifacts: dict[AsyncServer, dict[Address, ContextObject]] = (
            self.session._artifacts
        )
        new_artifacts: dict[AsyncServer, dict[Address, ContextObject]] = {}
        # spec buckets
        #     bucket by create, re-create, mutate, destroy
        #     moving contexts is a destroy and a create
        create_specs: dict[AsyncServer, dict[Address, Spec]] = {}
        mutate_specs: dict[AsyncServer, dict[Address, tuple[Spec, Spec]]] = {}
        destroy_specs: dict[AsyncServer, dict[Address, Spec]] = {}
        # create a set of visited components to ensure we only visit once
        visited_components: set[Component] = set()
        # iterate components depth-first
        #     might need different iteration strategies depending on initiating action
        #     a move affects the moved, and maybe feedback of any ins/outs
        #     while a channel count change can't be predicted except by iterating until no state changes occur
        #     but we can be inefficient for this first pass: don't over-engineer early
        # include related components (dependencies?) e.g. sends / receives / inputs / outputs
        #    anything that introduces cycles into the component digraph
        for component in self._walk():
            # for component in queue:
            #     resolve state
            #     resolve new specs
            #     compare new specs against cached specs
            #     bucket by context
            if component in visited_components:
                continue
            visited_components.add(component)
            old_specs = {spec.address: spec for spec in component._specs}
            # N.B. state is less important in this regime, but we do need to know
            #      for connections (sends, receives, inputs, outputs)
            #      because those introduce cyclic dependencies between components
            component._state = (new_state := component._resolve_state(context=context))
            component._specs = new_state.resolve_specs(
                component=component, context=context
            )
            new_specs = {spec.address: spec for spec in component._specs}
            for address, old_spec in old_specs.items():
                if new_spec := new_specs.pop(address, None):
                    # N.B.: recreation needs to know about the old ID so we know how to free it
                    #       thus we maintain two dicts of context artifacts
                    if old_spec.requires_recreation(new_spec):
                        destroy_specs.setdefault(old_spec.context, {})[
                            address
                        ] = old_spec
                        create_specs.setdefault(new_spec.context, {})[
                            address
                        ] = new_spec
                    else:
                        mutate_specs.setdefault(old_spec.context, {})[address] = (
                            old_spec,
                            new_spec,
                        )
                else:
                    destroy_specs.setdefault(old_spec.context, {})[address] = old_spec
            for address, new_spec in new_specs.items():
                create_specs.setdefault(new_spec.context, {})[address] = new_spec
        # once all specs bucketed, build digraph of create specs
        #   OK... WTF does this digraph look like...
        ...
        # create: walk digraph, executing specs against context
        #     if creating synthdefs, block until done
        for context, specs in create_specs.items():
            for spec in specs.values():
                spec.create(
                    context=context,
                    old_artifacts=old_artifacts[context],
                    new_artifacts=new_artifacts[context],
                )
        # mutate: iterate mutate/recreate specs in order
        for context, spec_pairs in mutate_specs.items():
            for old_spec, new_spec in spec_pairs.values():
                new_spec.mutate(
                    context=context,
                    old_artifacts=old_artifacts[context],
                    new_artifacts=new_artifacts[context],
                )
        # destroy: iterate destroy specs in order, special handling for "root" destroys (how?)
        for context, specs in destroy_specs.items():
            for spec in specs.values():
                spec.destroy(context=context, old_artifacts=old_artifacts[context])
        # merge artifcats
        for context, artifacts in old_artifacts.items():
            artifacts.update(new_artifacts[context])
        # return stuff, for debugging
        return create_specs, mutate_specs, destroy_specs

    def _resolve_initial_state(self) -> State:
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
            cast(Group, self._nodes[Names.GROUP]).dump_tree(),
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
