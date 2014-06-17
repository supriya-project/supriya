# -*- encoding: utf-8 -*-
from supriya.tools.servertools.AudioBus import AudioBus


class AudioOutputBus(AudioBus):
    r'''An audio output bus.

    ::

        >>> from supriya.tools import servertools
        >>> server = servertools.Server().boot()

    ::

        >>> output_bus = servertools.AudioOutputBus(server)
        >>> output_bus.channel_count
        8

    ::

        >>> output_bus.bus_id
        0

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### INITIALIZER ###

    def __init__(self, server):
        from supriya.tools import servertools
        assert isinstance(server, servertools.Server)
        assert server.server_options is not None
        server_options = server.server_options
        output_bus_channel_count = server_options.output_bus_channel_count
        if output_bus_channel_count < 1:
            raise ValueError
        AudioBus.__init__(
            self,
            channel_count=output_bus_channel_count,
            )
        self._bus_id = 0
        self._server = server

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.bus_proxies.__getitem__(item)
        elif isinstance(item, slice):
            indices = item.indices(len(self))
            start = indices[0]
            bus_id = self.bus_id + start
            channel_count = indices[1] - indices[0]
            return AudioBus(
                bus_id=bus_id,
                channel_count=channel_count,
                )
        raise TypeError

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass
