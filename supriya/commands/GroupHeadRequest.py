from supriya.commands.MoveRequest import MoveRequest
from supriya.commands.RequestId import RequestId


class GroupHeadRequest(MoveRequest):
    """
    A /g_head request.

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

        >>> request = supriya.commands.GroupHeadRequest([(synth, group)])
        >>> request.to_osc(True)
        OscMessage('/g_head', 1000, 1001)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     response = request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> response

    ::

        >>> for entry in transcript:
        ...     entry
        ...
        ('S', OscMessage(22, 1000, 1001))
        ('S', OscMessage(52, 1))
        ('R', OscMessage('/n_move', 1001, 1000, -1, 1002, 0))
        ('R', OscMessage('/synced', 1))

    ::

        >>> print(server.query_remote_nodes())
        NODE TREE 0 group
            1 group
                1000 group
                    1001 default
                    1002 group
                    1003 group

    ::

        >>> print(server.query_local_nodes())
        NODE TREE 0 group
            1 group
                1000 group
                    1001 default
                    1002 group
                    1003 group

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _target_first = True

    request_id = RequestId.GROUP_HEAD
