class NodeIDAllocator(object):
    r'''A node ID allocator.

    ::

        >>> from supriya.library import controllib
        >>> allocator = controllib.NodeIDAllocator()
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
        '_init_temp',
        '_mask',
        '_perm',
        '_perm_freed',
        '_temp',
        '_user',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        user=0,
        init_temp=1000,
        ):
        assert user <= 31
        self._init_temp = int(init_temp)
        self._user = int(user)
        self._mask = self._user << 26
        self._temp = self._init_temp
        self._perm = 2
        self._perm_freed = set()

    ### PUBLIC METHODS ###

    def allocate_node_id(self):
        x = self._temp
        temp = x + 1
        if 0x03FFFFFF < temp:
            temp = (temp % 0x03FFFFFF) + self._init_temp
        self._temp = temp
        x = x | self._mask
        return x

    def allocate_permanent_node_id(self):
        if self._perm_freed:
            x = min(self._perm_freed)
            self._perm_freed.remove(x)
        else:
            x = self._perm
            self._perm = min(x + 1, self._init_temp - 1)
        x = x | self._mask
        return x

    def free_permanent_node_id(self, node_id):
        node_id = node_id & 0x03FFFFFF
        if node_id < self._init_temp:
            self._perm_freed.add(node_id)
