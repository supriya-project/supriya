from supriya.commands.Response import Response


class NodeInfoResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_action',
        '_head_node_id',
        '_is_group',
        '_next_node_id',
        '_node_id',
        '_parent_group_id',
        '_previous_node_id',
        '_tail_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        action=None,
        node_id=None,
        parent_group_id=None,
        previous_node_id=None,
        next_node_id=None,
        is_group=None,
        head_node_id=None,
        tail_node_id=None,
        osc_message=None,
        ):
        import supriya.commands
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._action = supriya.commands.NodeAction.from_address(action)
        self._is_group = bool(is_group)
        self._head_node_id = self._coerce_node_id(head_node_id)
        self._next_node_id = self._coerce_node_id(next_node_id)
        self._node_id = self._coerce_node_id(node_id)
        self._parent_group_id = self._coerce_node_id(parent_group_id)
        self._previous_node_id = self._coerce_node_id(previous_node_id)
        self._tail_node_id = self._coerce_node_id(tail_node_id)

    ### PRIVATE METHODS ###

    def _coerce_node_id(self, node_id):
        if node_id is not None and -1 < node_id:
            return node_id
        return None

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action

    @property
    def head_node_id(self):
        return self._head_node_id

    @property
    def is_group(self):
        return self._is_group

    @property
    def next_node_id(self):
        return self._next_node_id

    @property
    def node_id(self):
        return self._node_id

    @property
    def parent_group_id(self):
        return self._parent_group_id

    @property
    def previous_node_id(self):
        return self._previous_node_id

    @property
    def tail_node_id(self):
        return self._tail_node_id
