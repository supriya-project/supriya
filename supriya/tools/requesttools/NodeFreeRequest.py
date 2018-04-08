import collections
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NodeFreeRequest(Request):
    """
    A /n_free request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.NodeFreeRequest(
        ...     node_ids=1000,
        ...     )
        >>> request
        NodeFreeRequest(
            node_ids=(1000,),
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(11, 1000)

    ::

        >>> message.address == requesttools.RequestId.NODE_FREE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_ids',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_ids=None
        ):
        Request.__init__(self)
        if not isinstance(node_ids, collections.Sequence):
            node_ids = (node_ids,)
        node_ids = tuple(int(_) for _ in node_ids)
        self._node_ids = node_ids

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        contents.extend(self.node_ids)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_ids(self):
        return self._node_ids

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.NODE_FREE
