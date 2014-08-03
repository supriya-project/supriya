# -*- encoding: utf-8 -*-
import collections
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NodeAfterRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id_pairs=None,
        ):
        from supriya.tools import requesttools
        Request.__init__(self)
        if node_id_pairs:
            if not isinstance(node_id_pairs, collections.Sequence):
                node_id_pairs = [node_id_pairs]
            prototype = requesttools.NodeIdPair
            assert all(isinstance(x, prototype) for x in node_id_pairs)
            node_id_pairs = tuple(node_id_pairs)
        self._node_id_pairs = node_id_pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        contents = [request_id]
        if self.node_id_pairs:
            for node_id_pair in self.node_id_pairs:
                contents.append(node_id_pair.node_id)
                contents.append(node_id_pair.target_node_id)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id_pairs(self):
        return self._node_id_pairs

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.NODE_AFTER