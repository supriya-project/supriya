# -*- encoding: utf-8 -*-
from supriya.tools.servertools.Bus import Bus


class AudioBus(Bus):
    r'''An audio bus.

    ::

        >>> from supriya.tools import servertools
        >>> server = servertools.Server().boot()

    ::

        >>> audio_bus = servertools.AudioBus(channel_count=4)
        >>> audio_bus.allocate()
        >>> audio_bus.bus_id
        16

    ::

        >>> audio_bus.map_symbol
        'a16'

    ::

        >>> audio_bus.free()
        >>> server.quit()
        RECV: OscMessage('/done', '/quit')
        <Server: offline>

    '''

    ### INITIALIZER ###

    def __init__(
        self,
        channel_count=1,
        ):
        Bus.__init__(
            self,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        Bus.allocate(self, server=server)
        bus_id = self.server.audio_bus_allocator.allocate()
        if bus_id is None:
            raise Exception
        assert bus_id not in self.server._audio_busses
        self.server._audio_busses[bus_id] = self
        self._bus_id = bus_id

    def free(self):
        if self.server is not None:
            self.server.audio_bus_allocator.free(self.bus_id)
            del(self.server._audio_busses[self._bus_id])
        self._bus_id = None
        Bus.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        r'''Gets this bus' calculation rate.
        
        ::

            >>> audio_bus = servertools.AudioBus()
            >>> audio_bus.calculation_rate
            <CalculationRate.AUDIO: 2>

        Returns calculation rate.
        '''
        from supriya.tools import synthdeftools
        return synthdeftools.CalculationRate.AUDIO
