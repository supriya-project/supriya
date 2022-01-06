import typing
from collections.abc import Sequence

import supriya.osc
from supriya.enums import RequestId

from .bases import Request


class MoveRequest(Request):

    ### CLASS VARIABLES ###

    class NodeIdPair(typing.NamedTuple):
        node_id: int
        target_node_id: int

    ### INITIALIZER ###

    def __init__(self, node_id_pairs=None):
        Request.__init__(self)
        if node_id_pairs:
            if not isinstance(node_id_pairs, Sequence):
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


class GroupHeadRequest(MoveRequest):
    """
    A /g_head request.

    ::

        >>> server = supriya.Server().boot()
        >>> group = supriya.Group().allocate(server)
        >>> synth = supriya.Synth().allocate(server)
        >>> group.extend([supriya.Group(), supriya.Group()])

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1000 group
                    1002 group
                    1003 group

    ::

        >>> request = supriya.commands.GroupHeadRequest([(synth, group)])
        >>> request.to_osc()
        OscMessage('/g_head', 1000, 1001)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     response = request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> response

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/g_head', 1000, 1001))
        ('S', OscMessage('/sync', 1))
        ('R', OscMessage('/n_move', 1001, 1000, -1, 1002, 0))
        ('R', OscMessage('/synced', 1))

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1000 group
                    1001 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1002 group
                    1003 group

    ::

        >>> print(server.root_node)
        NODE TREE 0 group
            1 group
                1000 group
                    1001 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1002 group
                    1003 group

    """

    ### CLASS VARIABLES ###

    _target_first = True

    request_id = RequestId.GROUP_HEAD


class GroupTailRequest(MoveRequest):
    """
    A /g_tail request.

    ::

        >>> server = supriya.Server().boot()
        >>> group = supriya.Group().allocate(server)
        >>> synth = supriya.Synth().allocate(server)
        >>> group.extend([supriya.Group(), supriya.Group()])

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1000 group
                    1002 group
                    1003 group

    ::

        >>> request = supriya.commands.GroupTailRequest([(synth, group)])
        >>> request.to_osc()
        OscMessage('/g_tail', 1000, 1001)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     response = request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> response

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/g_tail', 1000, 1001))
        ('S', OscMessage('/sync', 1))
        ('R', OscMessage('/n_move', 1001, 1000, 1003, -1, 0))
        ('R', OscMessage('/synced', 1))

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                    1003 group
                    1001 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5

    ::

        >>> print(server.root_node)
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                    1003 group
                    1001 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5

    """

    ### CLASS VARIABLES ###

    _target_first = True

    request_id = RequestId.GROUP_TAIL


class NodeAfterRequest(MoveRequest):
    """
    An /n_after request.

    ::

        >>> server = supriya.Server().boot()
        >>> group_a = supriya.Group([supriya.Group(), supriya.Group()])
        >>> group_b = supriya.Group([supriya.Group(), supriya.Group()])
        >>> synth_a = supriya.Synth()
        >>> synth_b = supriya.Synth()
        >>> server.default_group.extend([synth_a, synth_b, group_a, group_b])

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1002 group
                    1003 group
                    1004 group
                1005 group
                    1006 group
                    1007 group

    ::

        >>> request = supriya.commands.NodeAfterRequest(
        ...     [
        ...         [synth_a, group_a[-1]],
        ...         [synth_b, group_b],
        ...     ]
        ... )
        >>> request.to_osc()
        OscMessage('/n_after', 1000, 1004, 1001, 1005)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/n_after', 1000, 1004, 1001, 1005))
        ('S', OscMessage('/sync', 0))
        ('R', OscMessage('/n_move', 1000, 1002, 1004, -1, 0))
        ('R', OscMessage('/n_move', 1001, 1, 1005, -1, 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1002 group
                    1003 group
                    1004 group
                    1000 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1005 group
                    1006 group
                    1007 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5

    ::

        >>> print(server.root_node)
        NODE TREE 0 group
            1 group
                1002 group
                    1003 group
                    1004 group
                    1000 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1005 group
                    1006 group
                    1007 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5

    """

    ### CLASS VARIABLES ###

    _target_first = False

    request_id = RequestId.NODE_AFTER


class NodeBeforeRequest(MoveRequest):
    """
    An /n_before request.

    ::

        >>> server = supriya.Server().boot()
        >>> group_a = supriya.Group([supriya.Group(), supriya.Group()])
        >>> group_b = supriya.Group([supriya.Group(), supriya.Group()])
        >>> synth_a = supriya.Synth()
        >>> synth_b = supriya.Synth()
        >>> server.default_group.extend([synth_a, synth_b, group_a, group_b])

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1000 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1002 group
                    1003 group
                    1004 group
                1005 group
                    1006 group
                    1007 group

    ::

        >>> request = supriya.commands.NodeBeforeRequest(
        ...     [
        ...         [synth_a, group_a[0]],
        ...         [synth_b, group_b],
        ...     ]
        ... )
        >>> request.to_osc()
        OscMessage('/n_before', 1000, 1003, 1001, 1005)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/n_before', 1000, 1003, 1001, 1005))
        ('S', OscMessage('/sync', 0))
        ('R', OscMessage('/n_move', 1000, 1002, -1, 1003, 0))
        ('R', OscMessage('/n_move', 1001, 1, 1002, 1005, 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> print(server.query())
        NODE TREE 0 group
            1 group
                1002 group
                    1000 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1003 group
                    1004 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1005 group
                    1006 group
                    1007 group

    ::

        >>> print(server.root_node)
        NODE TREE 0 group
            1 group
                1002 group
                    1000 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1003 group
                    1004 group
                1001 default
                    out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                1005 group
                    1006 group
                    1007 group

    """

    ### CLASS VARIABLES ###

    _target_first = False

    request_id = RequestId.NODE_BEFORE
