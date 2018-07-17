import supriya.osc
from supriya.commands.Request import Request


class NodeRunRequest(Request):
    """
    A /n_run request.

    ::

        >>> import supriya
        >>> server = supriya.Server().boot()
        >>> synth_a = supriya.Synth().allocate()
        >>> synth_b = supriya.Synth().allocate()
        >>> synth_a.is_paused, synth_b.is_paused
        (False, False)

    Unpause ``synth_a`` (a no-op because it's already unpaused) and pause
    ``synth_b``:

    ::

        >>> request = supriya.commands.NodeRunRequest([
        ...     [synth_a, True],
        ...     [synth_b, False],
        ...     ])
        >>> request.to_osc_message(True)
        OscMessage('/n_run', 1000, 1, 1001, 0)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> for entry in transcript:
        ...     entry
        ...
        ('S', OscMessage(12, 1000, 1, 1001, 0))
        ('S', OscMessage(52, 0))
        ('R', OscMessage('/n_off', 1001, 1, -1, 1000, 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> synth_a.is_paused, synth_b.is_paused
        (False, True)

    Pause ``synth_a`` and unpause ``synth_b``:

    ::

        >>> request = supriya.commands.NodeRunRequest([
        ...     [synth_a, False],
        ...     [synth_b, True],
        ...     ])
        >>> request.to_osc_message(True)
        OscMessage('/n_run', 1000, 0, 1001, 1)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> for entry in transcript:
        ...     entry
        ...
        ('S', OscMessage(12, 1000, 0, 1001, 1))
        ('S', OscMessage(52, 1))
        ('R', OscMessage('/n_off', 1000, 1, 1001, -1, 0))
        ('R', OscMessage('/n_on', 1001, 1, -1, 1000, 0))
        ('R', OscMessage('/synced', 1))

    ::

        >>> synth_a.is_paused, synth_b.is_paused
        (True, False)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id_run_flag_pairs',
        )

    ### INITIALIZER ###

    def __init__(self, node_id_run_flag_pairs=None):
        Request.__init__(self)
        if node_id_run_flag_pairs:
            pairs = []
            for node_id, run_flag in node_id_run_flag_pairs:
                node_id = int(node_id)
                run_flag = bool(run_flag)
                pairs.append((node_id, run_flag))
            node_id_run_flag_pairs = tuple(pairs)
        self._node_id_run_flag_pairs = node_id_run_flag_pairs

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for node_id, run_flag in self.node_id_run_flag_pairs:
            node = server._nodes.get(node_id)
            if not node:
                continue
            node._run(run_flag)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.node_id_run_flag_pairs:
            for node_id, run_flag in self.node_id_run_flag_pairs:
                contents.append(node_id)
                contents.append(int(run_flag))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id_run_flag_pairs(self):
        return self._node_id_run_flag_pairs

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.NODE_RUN
