import supriya.osc
from .bases import Request
from supriya.enums import RequestId


class NodeQueryRequest(Request):
    """
    A /n_query request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.NodeQueryRequest(
        ...     node_id=1000,
        ...     )
        >>> request
        NodeQueryRequest(
            node_id=1000,
            )

    ::

        >>> request.to_osc()
        OscMessage('/n_query', 1000)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_QUERY

    ### INITIALIZER ###

    def __init__(self, node_id=None):
        Request.__init__(self)
        self._node_id = node_id

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = int(self.node_id)
        message = supriya.osc.OscMessage(request_id, node_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_patterns(self):
        return ["/n_info", self.node_id], ["/fail"]
