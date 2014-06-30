from supriya.tools.servertools.Node import Node


class Synth(Node):
    r'''A synth.

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> from supriya import synthdeftools
        >>> from supriya import ugentools
        >>> builder = synthdeftools.SynthDefBuilder(frequency=440)
        >>> sin_osc = ugentools.SinOsc.ar(
        ...     frequency=builder['frequency'],
        ...     ) * 0.0
        >>> out = ugentools.Out.ar(bus=(0, 1), source=sin_osc)
        >>> builder.add_ugen(out)
        >>> synthdef = builder.build()
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
