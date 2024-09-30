import asyncio
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Dict,
    Generator,
    Generic,
    Iterator,
    List,
    Literal,
    Optional,
    TypeAlias,
    TypeVar,
    cast,
)

from ..contexts import Buffer, BusGroup, Context, Group, Node
from ..contexts.responses import QueryTreeGroup
from ..enums import AddAction, BootStatus
from ..utils import iterate_nwise

C = TypeVar("C", bound="Component")

# TODO: Integrate this with channel logic
ChannelCount: TypeAlias = Literal[1, 2, 4, 8]

if TYPE_CHECKING:
    from .sessions import Session


class Component(Generic[C]):

    def __init__(
        self,
        *,
        parent: Optional[C] = None,
    ) -> None:
        self._lock = asyncio.Lock()
        self._parent: Optional[C] = parent

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

    def _iterate_parentage(self) -> Iterator["Component"]:
        component = self
        while component.parent is not None:
            yield component
            component = component.parent
        yield component

    def _walk(self) -> Generator["Component", None, None]:
        yield self

    @property
    def address(self) -> str:
        raise NotImplementedError

    @property
    def children(self) -> List["Component"]:
        raise NotImplementedError

    @property
    def graph_order(self) -> List[int]:
        graph_order = []
        for parent, child in iterate_nwise(reversed(list(self._iterate_parentage()))):
            graph_order.append(parent.children.index(child))
        return graph_order

    @property
    def parent(self) -> Optional[C]:
        return self._parent

    @property
    def session(self) -> Optional["Session"]:
        from .sessions import Session

        for component in self._iterate_parentage():
            if isinstance(component, Session):
                return component
        return None


class AllocatableComponent(Component, Generic[C]):

    def __init__(
        self,
        *,
        parent: Optional[C] = None,
    ) -> None:
        super().__init__(parent=parent)
        self._audio_buses: Dict[str, BusGroup] = {}
        self._buffers: Dict[str, Buffer] = {}
        self._context: Optional[Context] = None
        self._control_buses: Dict[str, BusGroup] = {}
        self._is_active: bool = True
        self._nodes: Dict[str, Node] = {}

    async def _activate(self) -> None:
        self._is_active = True
        if group := self._nodes.get("group"):
            group.unpause()
            group.set(active=1)

    def _allocate(
        self,
        *,
        add_action: AddAction = AddAction.ADD_TO_HEAD,
        context: Context,
        target_bus: BusGroup,
        target_node: Node,
    ) -> None:
        self._context = context

    def _can_allocate(self) -> bool:
        return (
            self._context is not None and self._context.boot_status == BootStatus.ONLINE
        )

    async def _deactivate(self) -> None:
        if group := self._nodes.get("group"):
            group.set(active=0)
        self._is_active = False

    def _deallocate(self) -> None:
        for key in tuple(self._audio_buses):
            self._audio_buses.pop(key).free()
        for key in tuple(self._control_buses):
            self._control_buses.pop(key).free()
        if group := self._nodes.get("group"):
            if not self._is_active:
                group.free()
            else:
                group.set(gate=0)
        self._nodes.clear()
        for key in tuple(self._buffers):
            self._buffers.pop(key).free()
        self._context = None

    def _delete(self) -> None:
        self._deallocate()
        self._parent = None
        self._session = None

    async def dump_tree(self) -> QueryTreeGroup:
        if self.session and self.session.status != BootStatus.ONLINE:
            raise RuntimeError
        annotations: Dict[int, str] = {}
        tree = await cast(
            Awaitable[QueryTreeGroup], cast(Group, self._nodes["group"]).dump_tree()
        )
        for component in self._walk():
            if not isinstance(component, AllocatableComponent):
                continue
            address = component.address
            for name, node in component._nodes.items():
                annotations[node.id_] = f"{address}:{name}"
        return tree.annotate(annotations)
