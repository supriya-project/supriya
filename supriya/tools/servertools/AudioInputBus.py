# -*- encoding: utf-8 -*-
from supriya.tools.servertools.AudioBus import AudioBus


class AudioInputBus(AudioBus):
    r'''An audio input bus.

    ::

        >>> from supriya.tools import servertools
        >>> server = servertools.Server().boot()
        >>> input_bus = servertools.AudioInputBus(server)
        >>> input_bus.channel_count
        8

    ::

        >>> input_bus.bus_id
        8

    ::

        >>> server.quit()
        RECV: OscMessage('/done', '/quit')
        <Server: offline>

    '''

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        assert isinstance(server, servertools.Server)
        assert server.server_options is not None
        server_options = server.server_options
        input_bus_channel_count = server_options.input_bus_channel_count
        output_bus_channel_count = server_options.output_bus_channel_count
        if input_bus_channel_count < 1:
            raise ValueError
        AudioBus.__init__(
            self,
            channel_count=input_bus_channel_count,
            )
        self._bus_id = output_bus_channel_count

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass
