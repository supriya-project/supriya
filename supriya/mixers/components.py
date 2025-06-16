import asyncio
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
from .specs import (
    Artifacts,
    Spec,
    SpecChange,
)

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
        self._connections: dict[tuple[Component, str], IO] = {}
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
        self._disconnect_parentage()

    def _disconnect_parentage(self) -> None:
        self._parent = None

    def _dump_components(self) -> list[str]:
        indent = "    "
        parts: list[str] = [repr(self)]
        for child in self.children:
            parts.extend(indent + line for line in child._dump_components())
        return parts

    def _gather_spec_changes(
        self,
        *,
        new_context: AsyncServer | None,
        old_context_artifacts: dict[AsyncServer, Artifacts],
    ) -> list[SpecChange]:
        old_specs = {spec.address: spec for spec in self._specs}
        self._specs = self._resolve_specs(
            context=new_context,
        )
        self._context = new_context
        new_specs = {spec.address: spec for spec in self._specs}
        return SpecChange.gather(
            old_specs=old_specs,
            new_specs=new_specs,
            old_context_artifacts=old_context_artifacts,
        )

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    async def _reconcile(
        self, *, context: AsyncServer | None, deleting: bool = False
    ) -> None:
        if self.session is None:
            raise ValueError
        # setup artifacts
        old_context_artifacts: dict[AsyncServer, Artifacts] = (
            self.session._context_artifacts
        )
        new_context_artifacts: dict[AsyncServer, Artifacts] = {
            context_: Artifacts() for context_ in old_context_artifacts
        }
        if context and context not in new_context_artifacts:
            new_context_artifacts[context] = Artifacts()
        # gather spec changes
        spec_changes: list[SpecChange] = []
        visited_components: set[Component] = set()
        related_components: list[Component] = []
        for component in self._walk():
            # need to patch up connected components
            related_components.extend(component._reconcile_connected_components())
            # need to know if we need to be deleted? how?
            # gather spec changes
            # add component to visited components to prevent cycles
            spec_changes.extend(
                component._gather_spec_changes(
                    new_context=context,
                    old_context_artifacts=old_context_artifacts,
                ),
            )
            visited_components.add(component)
        for component in related_components:
            if component in visited_components:
                continue
            # gather again
            spec_changes.extend(
                component._gather_spec_changes(
                    new_context=context,
                    old_context_artifacts=old_context_artifacts,
                ),
            )
        # sort and apply spec changes
        sorted_spec_changes = SpecChange.sort(spec_changes)
        for context_, spec_change_groups in sorted_spec_changes.items():
            for spec_change_group in spec_change_groups:
                spec_change_group.apply(
                    context=context_,
                    old_artifacts=old_context_artifacts[context_],
                    new_artifacts=new_context_artifacts[context_],
                    roots=[self],
                )
                if spec_change_group.sync:
                    await context_.sync()
        # merge artifacts
        for context_ in set(old_context_artifacts) | set(new_context_artifacts):
            old_context_artifacts[context_].merge(new_context_artifacts[context_])
        # ... actually we want a stack of components to delete here, because sends might get deleted too if deleting:
        if deleting:
            self._delete()

    def _reconcile_connected_components(self) -> list["Component"]:
        return []

    def _resolve_specs(self, context: AsyncServer | None) -> list[Spec]:
        return []

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
