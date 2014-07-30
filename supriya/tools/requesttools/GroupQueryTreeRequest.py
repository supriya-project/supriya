# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class GroupQueryTreeRequest(Request):
    r'''A /g_queryTree request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.GroupQueryTreeRequest(
        ...     node_id=0,
        ...     include_controls=True,
        ...     )
        >>> request
        GroupQueryTreeRequest(
            include_controls=True,
            node_id=0
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(57, 0, 1)

    ::

        >>> message.address == requesttools.RequestId.GROUP_QUERY_TREE
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_controls',
        '_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        include_controls=False,
        node_id=None,
        ):
        Request.__init__(self)
        self._node_id = node_id
        self._include_controls = bool(include_controls)

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        node_id = int(self.node_id)
        include_controls = int(self.include_controls)
        message = osctools.OscMessage(
            request_id,
            node_id,
            include_controls,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def include_controls(self):
        return self._include_controls

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.QueryTreeResponse: None,
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.GROUP_QUERY_TREE