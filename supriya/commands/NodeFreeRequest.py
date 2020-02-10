import collections

import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


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

        >>> request.to_osc()
        OscMessage('/n_free', 1000)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_FREE

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

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        contents.extend(self.node_ids)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_ids(self):
        return self._node_ids

    @property
    def response_patterns(self):
        return ["/n_end", int(self.node_ids[-1])], None
