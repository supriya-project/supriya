import supriya.osc
from supriya.tools.requesttools.Request import Request


class GroupNewRequest(Request):
    """
    A /g_new request.

    ::

        >>> from supriya.tools import requesttools
        >>> from supriya.tools import servertools
        >>> request = requesttools.GroupNewRequest(
        ...     add_action=servertools.AddAction.ADD_TO_TAIL,
        ...     node_id=1001,
        ...     target_node_id=1000,
        ...     )
        >>> request
        GroupNewRequest(
            add_action=AddAction.ADD_TO_TAIL,
            node_id=1001,
            target_node_id=1000,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(21, 1001, 1, 1000)

    ::

        >>> message.address == requesttools.RequestId.GROUP_NEW
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_add_action',
        '_node_id',
        '_target_node_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        node_id=None,
        target_node_id=None,
        ):
        from supriya.tools import servertools
        Request.__init__(self)
        self._add_action = servertools.AddAction.from_expr(add_action)
        self._node_id = node_id
        self._target_node_id = target_node_id

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        add_action = int(self.add_action)
        node_id = int(self.node_id)
        target_node_id = int(self.target_node_id)
        message = supriya.osc.OscMessage(
            request_id,
            node_id,
            add_action,
            target_node_id,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def add_action(self):
        return self._add_action

    @property
    def node_id(self):
        return self._node_id

    @property
    def target_node_id(self):
        return self._target_node_id

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.NodeInfoResponse: {
                'action': responsetools.NodeAction.NODE_CREATED,
                'node_id': self.node_id,
                },
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.GROUP_NEW
