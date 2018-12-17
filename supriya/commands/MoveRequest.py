import collections
import typing

import supriya.osc
from supriya.commands.Request import Request


class MoveRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ("_node_id_pairs",)

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

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.node_id_pairs:
            for node_id_pair in self.node_id_pairs:
                if self._target_first:
                    contents.append(int(node_id_pair.target_node_id))
                    contents.append(int(node_id_pair.node_id))
                else:
                    contents.append(int(node_id_pair.node_id))
                    contents.append(int(node_id_pair.target_node_id))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id_pairs(self):
        return self._node_id_pairs
