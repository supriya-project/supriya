# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NodeFreeRequest(Request):
    r'''A /n_free request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.NodeFreeRequest(
        ...     node_id=1000,
        ...     )
        >>> request
        NodeFreeRequest(
            node_id=1000
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(11, 1000)

    ::

        >>> message.address == requesttools.RequestId.NODE_FREE
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None
        ):
        self._node_id = node_id

    ### PUBLIC METHODS ###

    def to_osc_message(self):
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
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.NODE_FREE