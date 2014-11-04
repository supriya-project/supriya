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
        ...     ) * 0.5
        >>> out = ugentools.Out.ar(bus=(0, 1), source=sin_osc)
        >>> builder.add_ugen(out)
        >>> synthdef = builder.build()
        >>> synthdef.allocate(sync=True)
        <SynthDef: 49e59effd11f9576d6640f027e8410d6>

    ::

        >>> synth = servertools.Synth(synthdef=synthdef).allocate()

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_synthdef',
        '_synth_interface',
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
        self._synth_interface = servertools.SynthInterface(
            client=self,
            synthdef=self._synthdef,
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._synth_interface[item]

    ### PUBLIC METHODS ###

    def allocate(
        self,
        add_action=None,
        node_id_is_permanent=False,
        sync=True,
        target_node=None,
        **kwargs
        ):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            node_id_is_permanent=node_id_is_permanent,
            target_node=target_node,
            )
        message_bundler = servertools.MessageBundler(
            server=self.server,
            sync=sync,
            )
        with message_bundler:
            self.controls._set(**kwargs)
            settings, map_requests = self.controls.make_synth_new_settings()
            synth_request = requesttools.SynthNewRequest(
                add_action=add_action,
                node_id=node_id,
                synthdef=self.synthdef,
                target_node_id=target_node_id,
                **settings
                )
            if not self.synthdef.is_allocated:
                with servertools.MessageBundler(
                    send_to_server=False,
                    ) as synth_bundler:
                    synth_bundler.add_message(synth_request)
                    for map_request in map_requests:
                        synth_bundler.add_message(map_request)
                completion_message = synth_bundler.result
                print(repr(self.synthdef.server))
                synthdef_request = self.synthdef._allocate(
                    completion_message=completion_message,
                    server=self.server,
                    )
                message_bundler.add_message(synthdef_request)
                message_bundler.add_synchronizing_request(synthdef_request)
            else:
                message_bundler.add_message(synth_request)
                for map_request in map_requests:
                    message_bundler.add_message(map_request)
                message_bundler.add_synchronizing_request(synth_request)
        return self

    def free(
        self,
        send_to_server=True,
        ):
        Node.free(
            self,
            send_to_server=send_to_server,
            )
        #self._synth_interface.reset()

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        return self._synth_interface

    @property
    def synthdef(self):
        return self._synthdef