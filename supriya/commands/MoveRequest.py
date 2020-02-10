import collections
import typing

import supriya.osc
from supriya.commands.Request import Request


class MoveRequest(Request):

    ### CLASS VARIABLES ###

    class NodeIdPair(typing.NamedTuple):
        node_id: int
        target_node_id: int

    ### INITIALIZER ###

    def __init__(self, node_id_pairs=None):
        Request.__init__(self)
        if node_id_pairs:
            if not isinstance(node_id_pairs, collections.Sequence):
                node_id_pairs = [node_id_pairs]
            node_id_pairs = list(node_id_pairs)
            for i, x in enumerate(node_id_pairs):
                if not isinstance(x, self.NodeIdPair):
                    node_id_pairs[i] = self.NodeIdPair(*x)
            node_id_pairs = tuple(node_id_pairs)
        self._node_id_pairs = node_id_pairs

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        if self.node_id_pairs:
            for node_id_pair in self.node_id_pairs:
                target_node_id = self._sanitize_node_id(
                    node_id_pair.target_node_id, with_placeholders
                )
                node_id = self._sanitize_node_id(
                    node_id_pair.node_id, with_placeholders
                )
                if self._target_first:
                    contents.append(target_node_id)
                    contents.append(node_id)
                else:
                    contents.append(node_id)
                    contents.append(target_node_id)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id_pairs(self):
        return self._node_id_pairs
