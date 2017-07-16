from supriya.tools.responsetools.Response import Response


class NodeSetContiguousResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        items=None,
        osc_message=None,
        ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._items = items
        self._node_id = node_id

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    @property
    def node_id(self):
        return self._node_id
