from supriya.commands.MoveRequest import MoveRequest
from supriya.enums import RequestId


class GroupTailRequest(MoveRequest):
    """
    A /g_tail request.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> group = supriya.Group().allocate()
        >>> synth = supriya.Synth().allocate()
        >>> group.extend([supriya.Group(), supriya.Group()])

    ::

        >>> print(server.query_remote_nodes())
        NODE TREE 0 group
            1 group
                1001 default
                1000 group
                    1002 group
                    1003 group

    ::

        >>> request = supriya.commands.GroupTailRequest([(synth, group)])
        >>> request.to_osc(with_request_name=True)
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
        ('S', OscMessage(23, 1000, 1001))
        ('S', OscMessage(52, 1))
        ('R', OscMessage('/n_move', 1001, 1000, 1003, -1, 0))
        ('R', OscMessage('/synced', 1))

    ::

        >>> print(server.query_remote_nodes())
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                    1003 group
                    1001 default

    ::

        >>> print(server.query_local_nodes())
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                    1003 group
                    1001 default

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _target_first = True

    request_id = RequestId.GROUP_TAIL
