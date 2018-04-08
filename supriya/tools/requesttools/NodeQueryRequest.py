from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NodeQueryRequest(Request):
    """
    A /n_query request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.NodeQueryRequest(
        ...     node_id=1000,
        ...     )
        >>> request
        NodeQueryRequest(
            node_id=1000,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(46, 1000)

    ::

        >>> message.address == requesttools.RequestId.NODE_QUERY
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None
        ):
        Request.__init__(self)
        self._node_id = node_id

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        node_id = int(self.node_id)
        message = osctools.OscMessage(
            request_id,
            node_id,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.NODE_QUERY
