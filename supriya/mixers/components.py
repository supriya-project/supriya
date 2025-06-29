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
from .constants import IO, Address, ChannelCount, Names, Reconciliation
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
            return f"<{type(self).__name__} {self._id} {self._name!r}>"
        return f"<{type(self).__name__} {self._id}>"

    def _can_allocate(self) -> AsyncServer | None:
        if (
            context := self.context
        ) is not None and context.boot_status == BootStatus.ONLINE:
            return context
        return None

    def _delete(self) -> None:
        self._disconnect_parentage()

    def _disconnect_connections(
        self, roots: Optional[list["Component"]] = None
    ) -> tuple[list["Component"], set["Component"]]:
        related: list[Component] = []
        deleted: set[Component] = set()
        for component, _ in self._connections:
            if roots and any([root in component.parentage for root in roots]):
                continue
            related.append(component)
            if component._notify_disconnected(self):
                deleted.add(component)
        return related, deleted

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
        destroy_reconciliation: Reconciliation,
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
            destroy_reconciliation=destroy_reconciliation,
        )

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    def _notify_disconnected(self, connection: "Component") -> bool:
        """
        Determines if a connection should self-delete.

        E.g. a track is deleted, then a send from out-of-tree to that track
        should be deleted too. When the track is deleted, it calls
        _disconnect_connections(), which loops over its connections and calls
        _notify_disconnected on each.

        In practice, only sends get deleted in this way.
        """
        return False

    @classmethod
    async def _reconcile(
        cls,
        *,
        context: AsyncServer | None,
        deleting_components: list["Component"] | None = None,
        reconciling_components: list["Component"],
        session: Optional["Session"],
    ) -> None:
        # validate
        if session is None:
            raise RuntimeError
        # setup artifacts
        old_context_artifacts: dict[AsyncServer, Artifacts] = session._context_artifacts
        new_context_artifacts: dict[AsyncServer, Artifacts] = {
            context_: Artifacts() for context_ in old_context_artifacts
        }
        if context and context not in new_context_artifacts:
            new_context_artifacts[context] = Artifacts()
        # setup collections
        visited_components: set[Component] = set()
        related_components: list[Component] = []
        deleted_components: set[Component] = set(deleting_components or [])
        # gather spec changes
        spec_changes: list[SpecChange] = []
        # walk depth-first from the root
        for root in reconciling_components:
            deleting_ = root in (deleting_components or [])
            for component in root._walk():
                if component in visited_components:
                    continue
                # patch up cyclic relationships
                related, deleted = component._reconcile_connections(
                    deleting=deleting_, roots=reconciling_components
                )
                related_components.extend(related)
                deleted_components.update(deleted)
                # gather spec changes
                if deleting_:
                    destroy_reconciliation = (
                        Reconciliation.DESTROY_ROOT
                        if component is root
                        else Reconciliation.DESTROY
                    )
                else:
                    destroy_reconciliation = Reconciliation.DESTROY_SHALLOW
                spec_changes.extend(
                    component._gather_spec_changes(
                        new_context=None if deleting_ else context,
                        old_context_artifacts=old_context_artifacts,
                        destroy_reconciliation=destroy_reconciliation,
                    ),
                )
                visited_components.add(component)
        # omit visited components (walk once!) and sort by graph order
        related_components = sorted(
            set([x for x in related_components if x not in visited_components]),
            key=lambda x: x.graph_order,
        )
        # walk related components, but don't add new ones
        for component in related_components:
            # patch up cyclic relationships
            component._reconcile_connections(
                deleting=component in deleted_components, roots=reconciling_components
            )
            # gather spec changes
            spec_changes.extend(
                component._gather_spec_changes(
                    new_context=(
                        None if component in deleted_components else component._context
                    ),
                    old_context_artifacts=old_context_artifacts,
                    destroy_reconciliation=Reconciliation.DESTROY_SHALLOW,
                ),
            )
        # sort and apply spec changes
        sorted_spec_changes = SpecChange.sort(spec_changes)
        roots = [*reconciling_components, *deleted_components]
        for context_, spec_change_groups in sorted_spec_changes.items():
            for spec_change_group in spec_change_groups:
                spec_change_group.apply(
                    context=context_,
                    old_artifacts=old_context_artifacts[context_],
                    new_artifacts=new_context_artifacts[context_],
                    roots=roots,
                    related=related_components,
                )
                if spec_change_group.sync:
                    await context_.sync()
        # merge artifacts
        for context_ in set(old_context_artifacts) | set(new_context_artifacts):
            old_context_artifacts[context_].merge(new_context_artifacts[context_])
        # ... actually we want a stack of components to delete here, because sends might get deleted too if deleting:
        for component in sorted(
            deleted_components, key=lambda x: x.graph_order, reverse=True
        ):
            component._delete()

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: Optional[list["Component"]] = None,
    ) -> tuple[list["Component"], set["Component"]]:
        if deleting:
            return self._disconnect_connections(roots=roots)
        return [component for component, _ in self._connections], set()

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

    async def dump_tree(self, annotated: bool = True, numeric: bool = False) -> str:
        # TODO: Consolidate annotated and numeric flags.
        #       annotation: Literal["nested", "numeric"] | None
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
                if numeric:
                    address = component.numeric_address
                else:
                    address = component.address
                for name, node in component._artifacts.nodes.items():
                    annotations[node.id_] = f"{address}:{name}"
            return str(tree.annotate(annotations))
        return str(tree)

    @property
    def _nonrecursive_repr(self) -> str:
        return repr(self)

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
    def feedback_graph_order(self) -> tuple[int, ...]:
        """
        Graph order for sake of feedback calculations.
        """
        return self.graph_order

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
