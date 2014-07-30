# -*- encoding: utf-8 -*-
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
        >>> synthdef.allocate(sync=True)
        <SynthDef: 1fc2eec3eea3e5d30146f9c32097e429>

    ::

        >>> synth = servertools.Synth(synthdef=synthdef).allocate()

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        '_synth_control_group',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDef)
        Node.__init__(self)
        self._synthdef = synthdef
        self._synth_control_group = servertools.SynthControlGroup(
            client=self,
            synthdef=self._synthdef,
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._synth_control_group[item]

    ### PUBLIC METHODS ###

    def allocate(
        self,
        add_action=None,
        node_id_is_permanent=False,
        sync=False,
        target_node=None,
        **kwargs
        ):
        from supriya.tools import requesttools
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            node_id_is_permanent=node_id_is_permanent,
            target_node=target_node,
            )
        if not self.synthdef.is_allocated:
            self.synthdef.allocate(self.server)
        request = requesttools.SynthNewRequest(
            add_action=add_action,
            node_id=node_id,
            synthdef=self.synthdef,
            target_node_id=target_node_id,
            **kwargs
            )
        message = request.to_osc_message()
        for key, value in kwargs:
            self[key].set(value)
        self.server.send_message(message)
        if sync:
            self.server.sync()
        return self

    def free(
        self,
        send_to_server=True,
        ):
        Node.free(
            self,
            send_to_server=send_to_server,
            )
        self._synth_control_group.reset()

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        return self._synth_control_group

    @property
    def synthdef(self):
        return self._synthdef