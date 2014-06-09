class NodeIDAllocator(object):
    r'''A node ID allocator.

    ::

        >>> from supriya.tools import servertools
        >>> allocator = servertools.NodeIDAllocator()
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
        2
        3
        4

    ::

        >>> allocator.free_permanent_node_id(2)

    ::

        >>> allocator.allocate_permanent_node_id()
        2

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_initial_node_id',
        '_mask',
        '_next_permanent_id',
        '_freed_permanent_ids',
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
        self._next_permanent_id = 2
        self._freed_permanent_ids = set()

    ### PUBLIC METHODS ###

    def allocate_node_id(self):
        x = self._temp
        temp = x + 1
        if 0x03FFFFFF < temp:
            temp = (temp % 0x03FFFFFF) + self._initial_node_id
        self._temp = temp
        x = x | self._mask
        return x

    def allocate_permanent_node_id(self):
        if self._freed_permanent_ids:
            x = min(self._freed_permanent_ids)
            self._freed_permanent_ids.remove(x)
        else:
            x = self._next_permanent_id
            self._next_permanent_id = min(x + 1, self._initial_node_id - 1)
        x = x | self._mask
        return x

    def free_permanent_node_id(self, node_id):
        node_id = node_id & 0x03FFFFFF
        if node_id < self._initial_node_id:
            self._freed_permanent_ids.add(node_id)
