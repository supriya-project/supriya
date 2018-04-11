import threading
from supriya.system.SupriyaObject import SupriyaObject


class NodeIdAllocator(SupriyaObject):
    """
    A node ID allocator.

    ::

        >>> import supriya.realtime
        >>> allocator = supriya.realtime.NodeIdAllocator()
        >>> for _ in range(3):
        ...     allocator.allocate_node_id()
        ...
        1000
        1001
        1002

    ::

        >>> for _ in range(3):
        ...     allocator.allocate_permanent_node_id()
        ...
        1
        2
        3

    ::

        >>> allocator.free_permanent_node_id(2)

    ::

        >>> allocator.allocate_permanent_node_id()
        2

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_freed_permanent_ids',
        '_initial_node_id',
        '_lock',
        '_mask',
        '_next_permanent_id',
        '_temp',
        '_user_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        user_id=0,
        initial_node_id=1000,
        ):
        assert user_id <= 31
        self._initial_node_id = int(initial_node_id)
        self._user_id = int(user_id)
        self._mask = self._user_id << 26
        self._temp = self._initial_node_id
        self._next_permanent_id = 1
        self._freed_permanent_ids = set()
        self._lock = threading.Lock()

    ### PUBLIC METHODS ###

    def allocate_node_id(self):
        x = None
        with self._lock:
            x = self._temp
            temp = x + 1
            if 0x03FFFFFF < temp:
                temp = (temp % 0x03FFFFFF) + self._initial_node_id
            self._temp = temp
            x = x | self._mask
        return x

    def allocate_permanent_node_id(self):
        x = None
        with self._lock:
            if self._freed_permanent_ids:
                x = min(self._freed_permanent_ids)
                self._freed_permanent_ids.remove(x)
            else:
                x = self._next_permanent_id
                self._next_permanent_id = min(x + 1, self._initial_node_id - 1)
            x = x | self._mask
        return x

    def free_permanent_node_id(self, node_id):
        with self._lock:
            node_id = node_id & 0x03FFFFFF
            if node_id < self._initial_node_id:
                self._freed_permanent_ids.add(node_id)
