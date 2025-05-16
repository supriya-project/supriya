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

from ..contexts import AsyncServer, Group
from ..contexts.responses import QueryTreeGroup
from ..enums import BootStatus
from ..typing import DEFAULT, Default
from ..utils import iterate_nwise
from .specs import Address, Artifacts, Spec, SynthDefSpec

C = TypeVar("C", bound="Component")

if TYPE_CHECKING:
    from .mixers import Mixer
    from .sessions import Session


@dataclasses.dataclass
class State:

    def resolve_specs(
        self, component: "Component", context: AsyncServer | None
    ) -> list[Spec]:
        raise NotImplementedError


ChannelCount: TypeAlias = Literal[1, 2, 4, 8]


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
        self._channel_count: ChannelCount | Default = DEFAULT
        self._dependents: set[Component] = set()
        self._feedback_dependents: set[Component] = set()
        self._id = id_
        self._is_active = True
        self._lock = asyncio.Lock()
        self._name: str | None = name
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
        print(f"{self=}")
        print(f"{self.session=}")
        if self.session is None:
            raise ValueError
        # artifacts
        old_context_artifacts: dict[AsyncServer, Artifacts] = (
            self.session._context_artifacts
        )
        new_context_artifacts: dict[AsyncServer, Artifacts] = {
            context: Artifacts() for context in old_context_artifacts
        }
        if context and context not in new_context_artifacts:
            new_context_artifacts[context] = Artifacts()
        # spec buckets
        create_specs: dict[AsyncServer, dict[Address, Spec]] = {}
        mutate_specs: dict[AsyncServer, dict[Address, tuple[Spec, Spec]]] = {}
        destroy_specs: dict[AsyncServer, dict[Address, Spec]] = {}
        # create a set of visited components to ensure we only visit once
        visited_components: set[Component] = set()
        # iterate components depth-first
        # include related components (dependencies?) e.g. sends / receives / inputs / outputs
        #    anything that introduces cycles into the component digraph
        for component in self._walk():
            print(f"{component=}")
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
                    if new_spec.context and new_spec.requires_recreation(old_spec):
                        destroy_specs.setdefault(old_spec.context, {})[
                            address
                        ] = old_spec
                        create_specs.setdefault(new_spec.context, {})[
                            address
                        ] = new_spec
                    elif not new_spec.context:
                        destroy_specs.setdefault(old_spec.context, {})[
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
        dependents: dict[AsyncServer, dict[Address, list[Address]]] = {}
        dependencies: dict[AsyncServer, dict[Address, set[Address]]] = {}
        for context, specs in create_specs.items():
            for address, spec in specs.items():
                requirements = spec.requires()
                dependencies.setdefault(context, {}).setdefault(address, set()).update(
                    requirements
                )
                for requirement in requirements:
                    dependents.setdefault(context, {}).setdefault(
                        requirement, []
                    ).append(address)
        # debug
        print(f"{create_specs=}")
        print(f"{mutate_specs=}")
        print(f"{destroy_specs=}")
        print(f"{dependents=}")
        print(f"{dependencies=}")
        for context, d in dependents.items():
            for dx, dy in d.items():
                print(f"dependents: {dx} {dy}")
        for context, d in dependencies.items():
            for dx, dy in d.items():
                print(f"dependencies: {dx} {dy}")
        # create: walk digraph, executing specs against context
        #     if creating synthdefs, block until done
        for context, specs in create_specs.items():
            for spec in specs.values():
                spec.create(
                    context=context,
                    old_artifacts=old_context_artifacts.setdefault(
                        context, Artifacts()
                    ),
                    new_artifacts=new_context_artifacts.setdefault(
                        context, Artifacts()
                    ),
                )
                if isinstance(spec, SynthDefSpec):
                    await context.sync()
        # mutate: iterate mutate/recreate specs in order
        for context, spec_pairs in mutate_specs.items():
            for old_spec, new_spec in spec_pairs.values():
                new_spec.mutate(
                    context=context,
                    old_artifacts=old_context_artifacts[context],
                    new_artifacts=new_context_artifacts.setdefault(
                        context, Artifacts()
                    ),
                    old_spec=old_spec,
                )
        # destroy: iterate destroy specs in order, special handling for "root" destroys (how?)
        for context, specs in destroy_specs.items():
            for spec in specs.values():
                spec.destroy(
                    context=context, old_artifacts=old_context_artifacts[context]
                )
        # merge artifacts
        for context in set(old_context_artifacts) | set(new_context_artifacts):
            old_context_artifacts[context].merge(new_context_artifacts[context])
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
            # TODO: Reimplement this on top of Artifacts
            # for component in self._walk():
            #     address = component.address
            #     for name, node in component._nodes.items():
            #         annotations[node.id_] = f"{address}:{name}"
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
