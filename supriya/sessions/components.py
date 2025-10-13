from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Generator,
    Generic,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeAlias,
    TypeVar,
    cast,
    overload,
)

from ..contexts import AsyncServer, BusGroup, Group
from ..contexts.responses import QueryTreeGroup
from ..enums import AddAction, BootStatus
from ..typing import INHERIT, Inherit
from ..utils import iterate_nwise
from .constants import IO, Address, ChannelCount, Entities, Names, Reconciliation
from .specs import (
    Artifacts,
    GroupSpec,
    Spec,
    SpecChange,
    Specs,
)

C = TypeVar("C", bound="Component")

T = TypeVar("T", bound="Component")

SpecBucket: TypeAlias = dict[Address, tuple[Spec | None, Spec | None]]
ContextSpecBuckets: TypeAlias = dict[AsyncServer, SpecBucket]

if TYPE_CHECKING:
    from .mixers import Mixer
    from .parameters import Field, Parameter
    from .sessions import Session


class Component(Generic[C]):
    """
    The base class from which all components in a ``Session`` inherit.

    Provides tree-traversal, debugging, and state reconciliation logic.
    """

    def __init__(
        self,
        *,
        id_: int,
        name: str | None = None,
        parent: C | None = None,
    ) -> None:
        from .parameters import Parameter

        self._artifacts = Artifacts()
        self._channel_count: ChannelCount | Inherit = INHERIT
        self._connections: dict[tuple[Component, str], IO] = {}
        self._context: AsyncServer | None = None
        self._id: int = id_
        self._is_active: bool = True
        self._name: str | None = name
        self._parameters: dict[str, Parameter] = {}
        self._parent: C | None = parent
        self._specs: list[Spec] = []

    def __repr__(self) -> str:
        if self._name:
            return f"<{type(self).__name__} {self._id} {self._name!r}>"
        return f"<{type(self).__name__} {self._id}>"

    def _add_parameter(self, name: str, field: "Field") -> "Parameter":
        from .parameters import Parameter

        if name in self._parameters:
            raise ValueError(name)
        parameter = Parameter(
            component=self,
            name=name,
            field=field,
        )
        self._parameters[name] = parameter
        return parameter

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

    def _ensure_context(self) -> AsyncServer:
        if self.context is None:
            raise RuntimeError
        return self.context

    def _ensure_parent(self) -> C:
        if self.parent is None:
            raise RuntimeError
        return self.parent

    def _ensure_session(self) -> "Session":
        if self.session is None:
            raise RuntimeError
        return self.session

    def _gather_spec_changes(
        self,
        *,
        new_context: AsyncServer | None,
        old_context_artifacts: dict[AsyncServer, Artifacts],
        destroy_reconciliation: Reconciliation,
    ) -> list[SpecChange]:
        old_specs = {spec.address: spec for spec in self._specs}
        self._specs = list(self._resolve_specs(context=new_context))
        self._context = new_context
        new_specs = {spec.address: spec for spec in self._specs}
        return SpecChange.gather(
            old_specs=old_specs,
            new_specs=new_specs,
            old_context_artifacts=old_context_artifacts,
            destroy_reconciliation=destroy_reconciliation,
        )

    def _get_nested_address(self) -> str:
        raise NotImplementedError

    def _get_numeric_address(self) -> str:
        raise NotImplementedError

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    @property
    def _nonrecursive_repr(self) -> str:
        return repr(self)

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
        session: "Session",
    ) -> None:
        # treat offline contexts as null
        if context and not context.boot_status == BootStatus.ONLINE:
            context = None
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
            for component in root.walk(Component):
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
        # walk related compnthonents, but don't add new ones
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
        # update track activation, post deletion, as soloed tracks may have been deleted
        session._update_track_activation()

    def _reconcile_connections(
        self,
        *,
        deleting: bool = False,
        roots: Optional[list["Component"]] = None,
    ) -> tuple[list["Component"], set["Component"]]:
        if deleting:
            return self._disconnect_connections(roots=roots)
        return [component for component, _ in self._connections], set()

    def _resolve_container_spec(
        self,
        *,
        context: AsyncServer,
        destroy_strategy: Mapping[str, float] | None,
        parent: "Component",
        parent_container: Sequence["Component"],
        parent_container_group_name: str,
    ) -> GroupSpec:
        index: int = parent_container.index(self)
        if index:
            # relative to previous member's group
            group_add_action: AddAction = AddAction.ADD_AFTER
            group_target: Address = Spec.get_address(
                parent_container[index - 1],
                Entities.NODES,
                Names.GROUP,
            )
        else:
            # first member in the group
            group_add_action = AddAction.ADD_TO_HEAD
            group_target = Spec.get_address(
                parent, Entities.NODES, parent_container_group_name
            )
        return GroupSpec(
            add_action=group_add_action,
            component=self,
            context=context,
            destroy_strategy=dict(destroy_strategy) if destroy_strategy else None,
            name=Names.GROUP,
            parent_node=Spec.get_address(
                parent, Entities.NODES, parent_container_group_name
            ),
            target_node=group_target,
        )

    def _resolve_specs(self, context: AsyncServer | None) -> Specs:
        raise NotImplementedError

    def _set_parameter(self, name: str, value: float) -> bool:
        (parameter := self._parameters[name]).set(value)
        if not parameter._field.has_bus:
            return True
        return False

    def dump_components(self) -> str:
        """
        Dump the component's component tree as a string representation.
        """
        return "\n".join(self._dump_components())

    async def dump_tree(
        self, annotation: Literal["nested", "numeric"] | None = "nested"
    ) -> str:
        """
        Dump the component's node tree, optionally annotated, as a string representation.
        """
        if self._ensure_session().boot_status != BootStatus.ONLINE:
            raise RuntimeError
        tree = await cast(
            Awaitable[QueryTreeGroup],
            cast(Group, self._artifacts.nodes[Names.GROUP]).dump_tree(),
        )
        if annotation:
            annotations: dict[int, str] = {}
            for component in self.walk(Component):
                if annotation == "numeric":
                    address = component.numeric_address
                else:
                    address = component.address
                for name, node in component._artifacts.nodes.items():
                    annotations[node.id_] = f"{address}:{name}"
            return str(tree.annotate(annotations))
        return str(tree)

    async def set_parameter(self, name: str, value: float) -> None:
        """
        Set the component's named parameter to value.
        """
        async with (session := self._ensure_session())._lock:
            if self._set_parameter(name, value):
                await Component._reconcile(
                    context=self.context,
                    reconciling_components=[self],
                    session=session,
                )

    @overload
    def walk(self) -> Generator["Component", None, None]:
        pass

    @overload
    def walk(self, component_class: Type[T]) -> Generator[T, None, None]:
        pass

    def walk(
        self, component_class: Type["Component"] | None = None
    ) -> Generator["Component", None, None]:
        """
        Walk the subtree of components rooted at this component.
        """
        component_class_ = component_class or Component
        if isinstance(self, component_class_):
            yield self
        for child in self.children:
            yield from child.walk(component_class_)

    @property
    def address(self) -> Address:
        """
        Get the component's "nested" string address.

        Guaranteed to be unique, but may change if the structure of the
        component tree changes.
        """
        return self._get_nested_address()

    @property
    def channel_count(self) -> ChannelCount | Inherit:
        """
        Get the component's explicit channel count.
        """
        return self._channel_count

    @property
    def children(self) -> list["Component"]:
        """
        The component's child components.
        """
        return []

    @property
    def context(self) -> AsyncServer | None:
        """
        Get the component's ``Context``, if any.
        """
        return self._context

    @property
    def effective_channel_count(self) -> ChannelCount:
        """
        Get the component's implicit channel count.

        If the component's explicit channel count is ``Inherit``, inherit from
        the next non-default channel count in the component's parentage.
        """
        for component in self._iterate_parentage():
            if isinstance(channel_count := component.channel_count, int):
                return channel_count
        return 2

    @property
    def feedback_graph_order(self) -> tuple[int, ...]:
        """
        Get the component's graph order for sake of feedback calculations.
        """
        return self.graph_order

    @property
    def graph_order(self) -> tuple[int, ...]:
        """
        Get the component's graph order.
        """
        # TODO: Cache this
        graph_order = []
        for parent, child in iterate_nwise(reversed(list(self._iterate_parentage()))):
            graph_order.append(parent.children.index(child))
        return tuple(graph_order)

    @property
    def id(self) -> int:
        """
        Get the component's ID.
        """
        return self._id

    @property
    def mixer(self) -> Optional["Mixer"]:
        """
        Get the component's ``Mixer``, if any.
        """
        # TODO: Cache this
        from .mixers import Mixer

        for component in self._iterate_parentage():
            if isinstance(component, Mixer):
                return component
        return None

    @property
    def name(self) -> str | None:
        """
        Get the component's name.
        """
        return self._name

    @property
    def numeric_address(self) -> Address:
        """
        Get the component's "numeric" string address.

        Guaranteed to be unique and stable across structural mutations.
        """
        return self._get_numeric_address()

    @property
    def parameters(self) -> Mapping[str, "Parameter"]:
        """
        Get the component's parameters.
        """
        return MappingProxyType(self._parameters)

    @property
    def parent(self) -> C | None:
        """
        Get the component's parent component, if any.
        """
        return self._parent

    @property
    def parentage(self) -> list["Component"]:
        """
        Get the component's proper parentage, e.g. the component, its parent, its
        parent's parent, etc.
        """
        # TODO: Cache this
        return list(self._iterate_parentage())

    @property
    def session(self) -> Optional["Session"]:
        """
        Get the component's ``Session``, if any.
        """
        # TODO: Cache this
        from .sessions import Session

        for component in self._iterate_parentage():
            if isinstance(component, Session):
                return component
        return None


class ChannelSettable(Component[C]):
    async def set_channel_count(self, channel_count: ChannelCount | Inherit) -> None:
        """
        Set the component's channel count.
        """
        async with (session := self._ensure_session())._lock:
            self._channel_count = channel_count
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )


class Deletable(Component[C]):
    async def delete(self) -> None:
        """
        Delete the component.
        """
        async with (session := self._ensure_session())._lock:
            await Component._reconcile(
                context=None,
                deleting_components=[self],
                reconciling_components=[self],
                session=session,
            )


class Movable(Component[C]):
    def _move(self, *, new_parent: C, index: int) -> None:
        raise NotImplementedError

    async def move(self, parent: C, index: int) -> None:
        """
        Move the component to another container and/or index in a container.
        """
        async with (session := self._ensure_session())._lock:
            self._move(new_parent=parent, index=index)
            await Component._reconcile(
                context=self.context,
                reconciling_components=[self],
                session=session,
            )


class NameSettable(Component[C]):
    def set_name(self, name: str | None = None) -> None:
        """
        Set the components's name.
        """
        self._name = name


class LevelsCheckable(Component[C]):
    def _get_input_levels_bus_group(self) -> BusGroup:
        return self._artifacts.control_buses[Names.INPUT_LEVELS]

    def _get_output_levels_bus_group(self) -> BusGroup:
        return self._artifacts.control_buses[Names.OUTPUT_LEVELS]

    @property
    def input_levels(self) -> list[float]:
        """
        Get the component's current input levels.

        Read from server shared memory.
        """
        if not (shared_memory := self._ensure_context()._shared_memory):
            raise RuntimeError
        return shared_memory[self._get_input_levels_bus_group()]

    @property
    def output_levels(self) -> list[float]:
        """
        Get the component's current output levels.

        Read from server shared memory.
        """
        if not (shared_memory := self._ensure_context()._shared_memory):
            raise RuntimeError
        return shared_memory[self._get_output_levels_bus_group()]
