from supriya.commands.GroupNewRequest import GroupNewRequest


class ParallelGroupNewRequest(GroupNewRequest):
    """
    A /p_new request.

    ..  note::  This behaves like a ``/g_new`` request when run on ``scsynth``
                instead of ``supernova``.

    ::

        >>> import supriya
        >>> server = supriya.Server().boot()
        >>> group = supriya.Group().allocate()

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group

    ::

        >>> request = supriya.commands.ParallelGroupNewRequest(
        ...     add_action=supriya.realtime.AddAction.ADD_TO_TAIL,
        ...     node_id=1001,
        ...     target_node_id=1,
        ...     )
        >>> request.to_osc_message(True)
        OscMessage('/p_new', 1001, 1, 1)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     response = request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> response
        NodeInfoResponse(
            action=NodeAction.NODE_CREATED,
            is_group=True,
            node_id=1001,
            parent_group_id=1,
            previous_node_id=1000,
            )

    ::

        >>> for entry in transcript:
        ...     entry
        ...
        ('S', OscMessage(63, 1001, 1, 1))
        ('R', OscMessage('/n_go', 1001, 1, 1000, -1, 1, -1, -1))
        ('S', OscMessage(52, 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group
                1001 group

    ::

        >>> print(server.query_local_nodes())
        NODE TREE 0 group
            1 group
                1000 group
                1001 group

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC PROPERTIES ###

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.PARALLEL_GROUP_NEW
