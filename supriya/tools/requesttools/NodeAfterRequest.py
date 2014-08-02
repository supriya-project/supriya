# -*- encoding: utf-8 -*-
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
        Request.__init__(self)
        if node_id_pairs:
            pairs = []
            for node_id, target_node_id in node_id_pairs:
                node_id = int(node_id)
                target_node_id = int(target_node_id)
                pair = (node_id, target_node_id)
                pairs.append(pair)
            node_id_pairs = tuple(pairs)
        self._node_id_pairs = node_id_pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        contents = [request_id]
        if self.node_id_pairs:
            for pair in self.node_id_pairs:
                contents.extend(pair)
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