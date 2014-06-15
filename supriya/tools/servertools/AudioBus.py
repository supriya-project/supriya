# -*- encoding: utf-8 -*-
from supriya.tools.servertools.Bus import Bus


class AudioBus(Bus):

    def __init__(
        self,
        channel_count,
        ):
        Bus.__init__(
            self,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        super(self, Bus).allocate(self, server=server)
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
        super(self, Bus).free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        from supriya.tools import synthdeftools
        return synthdeftools.CalculationRate.AUDIO
