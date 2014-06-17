from supriya.tools.servertools.Node import Node


class Synth(Node):
    r'''A synth.

    ::

        >>> from supriya import servertools
        >>> from supriya import synthdeftools
        >>> server = servertools.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> synthdef = synthdeftools.SynthDef('test', frequency=440)
        >>> controls = synthdef.controls
        >>> sin_osc = synthdeftools.SinOsc.ar(
        ...     frequency=controls['frequency'],
        ...     ) * 0.0
        >>> out = synthdeftools.Out.ar(bus=(0, 1), source=sin_osc)
        >>> synthdef.add_ugen(out)
        >>> synthdef.allocate()
        >>> server.sync()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> synth = servertools.Synth(synthdef=synthdef).allocate()

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef,
        ):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, (str, synthdeftools.SynthDef))
        Node.__init__(self)
        self._synthdef = synthdef

    ### PUBLIC METHODS ###

    def allocate(
        self,
        add_action=None,
        node_id_is_permanent=False,
        target_node=None,
        **kwargs
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            node_id_is_permanent=node_id_is_permanent,
            target_node=target_node,
            )
        synthdef_name = self.synthdef
        if isinstance(self.synthdef, synthdeftools.SynthDef):
            synthdef_name = synthdef_name.actual_name
        message = servertools.CommandManager.make_synth_new_message(
            add_action=add_action,
            node_id=node_id,
            synthdef_name=synthdef_name,
            target_node_id=target_node_id,
            **kwargs
            )
        self.server.send_message(message)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
