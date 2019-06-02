import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class GroupFreeAllRequest(Request):
    """
    A /g_freeAll request.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> group = supriya.Group().allocate()
        >>> group.extend([supriya.Synth(), supriya.Group()])
        >>> group[1].extend([supriya.Synth(), supriya.Group()])
        >>> group[1][1].extend([supriya.Synth(), supriya.Group()])

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group
                    1001 default
                        out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                    1002 group
                        1003 default
                            out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                        1004 group
                            1005 default
                                out: 0.0, amplitude: 0.1, frequency: 440.0, gate: 1.0, pan: 0.5
                            1006 group

    ::

        >>> request = supriya.commands.GroupFreeAllRequest(group)
        >>> request.to_osc(with_request_name=True)
        OscMessage('/g_freeAll', 1000)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage(24, 1000))
        ('S', OscMessage(52, 2))
        ('R', OscMessage('/n_end', 1001, -1, -1, -1, 0))
        ('R', OscMessage('/n_end', 1003, -1, -1, -1, 0))
        ('R', OscMessage('/n_end', 1005, -1, -1, -1, 0))
        ('R', OscMessage('/n_end', 1006, -1, -1, -1, 1, -1, -1))
        ('R', OscMessage('/n_end', 1004, -1, -1, -1, 1, -1, -1))
        ('R', OscMessage('/n_end', 1002, -1, -1, -1, 1, -1, -1))
        ('R', OscMessage('/synced', 2))

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group

    ::

        >>> print(server.query_local_nodes(True))
        NODE TREE 0 group
            1 group
                1000 group

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_group_id",)

    request_id = RequestId.GROUP_FREE_ALL

    ### INITIALIZER ###

    def __init__(self, group_id):
        Request.__init__(self)
        self._group_id = group_id

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        group_id = int(self.group_id)
        message = supriya.osc.OscMessage(request_id, group_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def group_id(self):
        return self._group_id
