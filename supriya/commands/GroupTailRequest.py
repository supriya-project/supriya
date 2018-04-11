import collections
import supriya.osc
from supriya.commands.Request import Request


class GroupTailRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id_pairs=None,
        ):
        import supriya.commands
        Request.__init__(self)
        if node_id_pairs:
            if not isinstance(node_id_pairs, collections.Sequence):
                node_id_pairs = [node_id_pairs]
            prototype = supriya.commands.NodeIdPair
            assert all(isinstance(x, prototype) for x in node_id_pairs)
            node_id_pairs = tuple(node_id_pairs)
        self._node_id_pairs = node_id_pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.node_id_pairs:
            for node_id_pair in self.node_id_pairs:
                contents.append(node_id_pair.target_node_id)
                contents.append(node_id_pair.node_id)
        message = supriya.osc.OscMessage(*contents)
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
        import supriya.commands
        return supriya.commands.RequestId.GROUP_TAIL
