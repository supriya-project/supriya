import collections
import supriya.osc
from supriya.commands.Request import Request


class GroupTailRequest(Request):
    """
    A /g_tail request.

    ::

        >>> import supriya
        >>> server = supriya.Server().boot()
        >>> group = supriya.Group().allocate()
        >>> synth = supriya.Synth().allocate()
        >>> group.extend([supriya.Group(), supriya.Group()])

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1000 group
                    1002 group
                    1003 group

    ::

        >>> request = supriya.commands.GroupTailRequest([(synth, group)])
        >>> request.to_osc_message(True)
        OscMessage('/g_tail', 1000, 1001)

    ::

        >>> request.communicate(server=server)

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                    1003 group
                    1001 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id_pairs',
        )

    ### INITIALIZER ###

    def __init__(self, node_id_pairs=None):
        import supriya.commands
        Request.__init__(self)
        if node_id_pairs:
            if not isinstance(node_id_pairs, collections.Sequence):
                node_id_pairs = [node_id_pairs]
            node_id_pairs = list(node_id_pairs)
            for i, x in enumerate(node_id_pairs):
                if not isinstance(x, supriya.commands.NodeIdPair):
                    node_id_pairs[i] = supriya.commands.NodeIdPair(*x)
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
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.GROUP_TAIL
