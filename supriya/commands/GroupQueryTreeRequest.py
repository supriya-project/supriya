import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class GroupQueryTreeRequest(Request):
    """
    A /g_queryTree request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.GroupQueryTreeRequest(
        ...     node_id=0,
        ...     include_controls=True,
        ...     )
        >>> request
        GroupQueryTreeRequest(
            include_controls=True,
            node_id=0,
            )

    ::

        >>> request.to_osc()
        OscMessage('/g_queryTree', 0, 1)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.GROUP_QUERY_TREE

    ### INITIALIZER ###

    def __init__(self, node_id=None, include_controls=False):
        Request.__init__(self)
        self._node_id = node_id
        self._include_controls = bool(include_controls)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = int(self.node_id)
        include_controls = int(self.include_controls)
        message = supriya.osc.OscMessage(request_id, node_id, include_controls)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def include_controls(self):
        return self._include_controls

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_patterns(self):
        return ["/g_queryTree.reply", int(self.include_controls), self.node_id], None
