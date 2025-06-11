import asyncio
import contextlib
import itertools
from collections import deque
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Generator,
    Generic,
    Iterator,
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
from .constants import IO, Address, ChannelCount, Names
from .specs import Artifacts, BufferSpec, BusSpec, NodeSpec, Spec, SynthDefSpec

C = TypeVar("C", bound="Component")

SpecBucket: TypeAlias = dict[Address, tuple[Spec | None, Spec | None]]
ContextSpecBuckets: TypeAlias = dict[AsyncServer, SpecBucket]

if TYPE_CHECKING:
    from .mixers import Mixer
    from .sessions import Session


class Component(Generic[C]):
    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: C | None = None,
    ) -> None:
        self._artifacts = Artifacts()
        self._channel_count: ChannelCount | Default = DEFAULT
        self._dependencies: dict[tuple[Component, str], IO] = {}
        self._id = id_
        self._is_active = True
        self._lock = asyncio.Lock()
        self._name: str | None = name
        self._parent: C | None = parent
        self._specs: list[Spec] = []
        # TODO: We wanna cache the context, because that makes some things simpler
        #       e.g. checking if the context has changed...
        #       are we booting? quitting? just mutating? changing contexts?
        self._context: AsyncServer | None = None

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

    def _gather_component_specs(
        self,
        *,
        component: "Component",
        new_context: AsyncServer | None,
        create_spec_buckets: ContextSpecBuckets,
        destroy_spec_buckets: ContextSpecBuckets,
        mutate_spec_buckets: ContextSpecBuckets,
        rooted: bool,
    ) -> None:
        # old_context = component._context
        old_specs = {spec.address: spec for spec in component._specs}
        component._specs = component._resolve_specs(
            context=new_context,
        )
        component._context = new_context
        new_specs = {spec.address: spec for spec in component._specs}
        for address, old_spec in old_specs.items():
            if not old_spec.context:
                raise RuntimeError
            if new_spec := new_specs.pop(address, None):
                # N.B.: recreation needs to know about the old ID so we know how to free it
                #       thus we maintain two dicts of context artifacts
                if new_spec.context and new_spec.requires_recreation(old_spec):
                    destroy_spec_buckets[old_spec.context][address] = (old_spec, None)
                    create_spec_buckets[new_spec.context][address] = (None, new_spec)
                elif not new_spec.context:
                    destroy_spec_buckets[old_spec.context][address] = (new_spec, None)
                else:
                    mutate_spec_buckets[old_spec.context][address] = (
                        old_spec,
                        new_spec,
                    )
            else:
                destroy_spec_buckets[old_spec.context][address] = (old_spec, None)
        for address, new_spec in new_specs.items():
            if not new_spec.context:
                raise RuntimeError
            create_spec_buckets[new_spec.context][address] = (None, new_spec)

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    async def _process_create_specs(
        self,
        spec_buckets: ContextSpecBuckets,
        old_context_artifacts: dict[AsyncServer, Artifacts],
        new_context_artifacts: dict[AsyncServer, Artifacts],
    ) -> None:
        def create_specs(
            *,
            context: AsyncServer,
            specs: list[list[Spec]],
            group: bool,
        ) -> None:
            if not specs:
                return
            for spec_group in specs:
                with contextlib.ExitStack() as exit_stack:
                    if group:
                        exit_stack.enter_context(context.at())
                    for spec in spec_group:
                        spec.create(
                            context=context,
                            old_artifacts=old_context_artifacts[context],
                            new_artifacts=new_context_artifacts[context],
                        )

        # create: walk digraph, executing specs against context
        #     if creating synthdefs, block until done
        for context, specs in spec_buckets.items():
            (
                buffer_specs,
                bus_specs,
                node_specs,
                synthdef_specs,
            ) = self._sort_create_specs(specs)
            # make sure synthdefs are filtered by only the new ones for that context
            synthdef_specs = [
                synthdef_spec
                for synthdef_spec in synthdef_specs
                if synthdef_spec.address not in old_context_artifacts[context].synthdefs
            ]
            create_specs(context=context, specs=[synthdef_specs], group=False)
            create_specs(context=context, specs=buffer_specs, group=True)
            if synthdef_specs or buffer_specs:
                await context.sync()
            create_specs(context=context, specs=bus_specs, group=True)
            create_specs(context=context, specs=node_specs, group=True)

    def _process_mutate_specs(
        self,
        spec_buckets: ContextSpecBuckets,
        old_context_artifacts: dict[AsyncServer, Artifacts],
        new_context_artifacts: dict[AsyncServer, Artifacts],
    ) -> None:
        for context, specs in spec_buckets.items():
            for old_spec, new_spec in specs.values():
                assert old_spec and new_spec
                new_spec.mutate(
                    context=context,
                    old_artifacts=old_context_artifacts[context],
                    new_artifacts=new_context_artifacts.setdefault(
                        context, Artifacts()
                    ),
                    old_spec=old_spec,
                )

    def _process_destroy_specs(
        self,
        spec_buckets: ContextSpecBuckets,
        old_context_artifacts: dict[AsyncServer, Artifacts],
    ) -> None:
        # destroy: iterate destroy specs in order, special handling for "root" destroys (how?)
        for context, specs in spec_buckets.items():
            for old_spec, _ in specs.values():
                assert old_spec
                old_spec.destroy(
                    context=context, old_artifacts=old_context_artifacts[context]
                )

    async def _reconcile(
        self, *, context: AsyncServer | None, deleting: bool = False
    ) -> None:
        if self.session is None:
            raise ValueError
        # artifacts
        old_context_artifacts, new_context_artifacts = self._resolve_context_artifacts(
            context=context, session=self.session
        )
        # spec buckets
        create_spec_buckets: ContextSpecBuckets = {
            ctx: {} for ctx in new_context_artifacts
        }
        mutate_spec_buckets: ContextSpecBuckets = {
            ctx: {} for ctx in new_context_artifacts
        }
        destroy_spec_buckets: ContextSpecBuckets = {
            ctx: {} for ctx in new_context_artifacts
        }
        # iterate components depth-first
        # include related components (dependencies?) e.g. sends / receives / inputs / outputs
        #    anything that introduces cycles into the component digraph
        visited_components: set[Component] = set()
        related_components: list[Component] = []
        for component in self._walk():
            related_components.extend(component._reconcile_dependents())
            self._gather_component_specs(
                component=component,
                new_context=context,
                create_spec_buckets=create_spec_buckets,
                destroy_spec_buckets=destroy_spec_buckets,
                mutate_spec_buckets=mutate_spec_buckets,
                rooted=component is self,
            )
            visited_components.add(component)
        for component in related_components:
            if component in visited_components:
                continue
            self._gather_component_specs(
                component=component,
                new_context=context,
                create_spec_buckets=create_spec_buckets,
                destroy_spec_buckets=destroy_spec_buckets,
                mutate_spec_buckets=mutate_spec_buckets,
                rooted=True,
            )
            visited_components.add(component)
        # process specs
        await self._process_create_specs(
            create_spec_buckets, old_context_artifacts, new_context_artifacts
        )
        self._process_mutate_specs(
            mutate_spec_buckets, old_context_artifacts, new_context_artifacts
        )
        self._process_destroy_specs(destroy_spec_buckets, old_context_artifacts)
        # merge artifacts
        for context in set(old_context_artifacts) | set(new_context_artifacts):
            old_context_artifacts[context].merge(new_context_artifacts[context])
        # destroy
        # ... actually we want a stack of components to delete here, because sends might get deleted too
        if deleting:
            self._delete()

    def _reconcile_dependents(self) -> list["Component"]:
        return []

    def _resolve_context_artifacts(
        self,
        context: AsyncServer | None,
        session: "Session",
    ) -> tuple[dict[AsyncServer, Artifacts], dict[AsyncServer, Artifacts]]:
        old_context_artifacts: dict[AsyncServer, Artifacts] = session._context_artifacts
        new_context_artifacts: dict[AsyncServer, Artifacts] = {
            context_: Artifacts() for context_ in old_context_artifacts
        }
        if context and context not in new_context_artifacts:
            new_context_artifacts[context] = Artifacts()
        return old_context_artifacts, new_context_artifacts

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        return []

    @classmethod
    def _sort_create_specs(
        cls, specs: SpecBucket
    ) -> tuple[
        list[list[Spec]],
        list[list[Spec]],
        list[list[Spec]],
        list[Spec],
    ]:
        buffer_specs: dict[Component, list[Spec]] = {}
        bus_specs: dict[Component, list[Spec]] = {}
        synthdef_specs: list[Spec] = []
        ordered_node_specs: dict[Address, Spec] = {}
        unordered_node_specs: deque[tuple[Spec, set[Address]]] = deque()
        for _, spec in specs.values():
            assert spec
            if isinstance(spec, BufferSpec):
                buffer_specs.setdefault(spec.component, []).append(spec)
            elif isinstance(spec, BusSpec):
                bus_specs.setdefault(spec.component, []).append(spec)
            elif isinstance(spec, SynthDefSpec):
                synthdef_specs.append(spec)
            elif isinstance(spec, NodeSpec):
                dependencies: set[Address] = set(
                    [
                        address
                        for address in spec.requires()
                        if f":{Names.NODES}:" in address and address in specs
                    ]
                )
                unordered_node_specs.append((spec, dependencies))
        while unordered_node_specs:
            node_spec, dependencies = unordered_node_specs.popleft()
            if all(dependency in ordered_node_specs for dependency in dependencies):
                ordered_node_specs[node_spec.address] = node_spec
            else:
                unordered_node_specs.append((node_spec, dependencies))

        # synthdefs, alphabetical
        # busses, alphabetical, grouped by component in graph order
        # waves of nodes, grouped by component in graph order
        #     component might repeat
        return (
            list(buffer_specs.values()),
            list(bus_specs.values()),
            [
                list(group)
                for _, group in itertools.groupby(
                    ordered_node_specs.values(), lambda x: x.component
                )
            ],
            sorted(synthdef_specs, key=lambda x: x.address),
        )

    def _walk(
        self, component_class: Type["Component"] | None = None
    ) -> Generator["Component", None, None]:
        component_class_ = component_class or Component
        if isinstance(self, component_class_):
            yield self
        for child in self.children:
            yield from child._walk(component_class_)

    def _walk_related(self) -> Generator["Component", None, None]:
        """
        Walk subtree and reconcile related components at the same time.
        """
        visited_components: set[Component] = set()
        related_components: list[Component] = []
        for component in self._walk():
            related_components.extend(component._reconcile_dependents())
            yield component
            visited_components.add(component)
        for component in related_components:
            if component in visited_components:
                continue
            yield component
            visited_components.add(component)

    def dump_components(self) -> str:
        return "\n".join(self._dump_components())

    async def dump_tree(self, annotated: bool = True) -> str:
        if self.session and self.session.status != BootStatus.ONLINE:
            raise RuntimeError
        tree = await cast(
            Awaitable[QueryTreeGroup],
            cast(Group, self._artifacts.nodes[Names.GROUP]).dump_tree(),
        )
        if annotated:
            annotations: dict[int, str] = {}
            # TODO: Reimplement this on top of Artifacts
            for component in self._walk():
                address = component.address
                for name, node in component._artifacts.nodes.items():
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
