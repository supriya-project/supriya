import collections
import supriya.osc
from supriya.commands.Request import Request


class NodeFreeRequest(Request):
    """
    A /n_free request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.NodeFreeRequest(
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

        >>> message.address == supriya.commands.RequestId.NODE_FREE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_ids',
        )

    ### INITIALIZER ###

    def __init__(self, node_ids=None):
        Request.__init__(self)
        if not isinstance(node_ids, collections.Sequence):
            node_ids = (node_ids,)
        node_ids = tuple(int(_) for _ in node_ids)
        self._node_ids = node_ids

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for node_id in self.node_ids:
            node = server._nodes.get(node_id)
            if not node:
                continue
            node._set_parent(None)
            node._unregister_with_local_server()

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        contents.extend(self.node_ids)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_ids(self):
        return self._node_ids

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.NODE_FREE
