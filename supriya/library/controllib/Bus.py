# -*- encoding: utf-8 -*-
from supriya.library.controllib.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy):
    r'''A bus.

    ::

        >>> from supriya import audiolib
        >>> from supriya import controllib
        >>> bus = controllib.Bus(
        ...    calculation_rate=audiolib.CalculationRate.AUDIO,
        ...    channel_count=1,
        ...    )

    '''
    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_index',
        '_calculation_rate',
        '_channel_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=1,
        ):
        from supriya.library import audiolib
        ServerObjectProxy.__init__(self)
        if calculation_rate is None:
            calculation_rate = audiolib.CalculationRate.AUDIO
        assert calculation_rate in (
            audiolib.CalculationRate.AUDIO,
            audiolib.CalculationRate.CONTROL,
            )
        self._calculation_rate = calculation_rate
        self._channel_count = int(channel_count)
        self._bus_index = None

    ### PUBLIC METHODS ###

    def allocate(self, server_session=None):
        from supriya.library import audiolib
        ServerObjectProxy.allocate(self)
        channel_count = self.channel_count
        if self.calculation_rate == audiolib.CalculationRate.AUDIO:
            bus_index = server_session.audio_bus_allocator.allocate(
                channel_count)
        else:
            bus_index = server_session.control_bus_allocator.allocate(
                channel_count)
        if bus_index is None:
            raise Exception
        self._bus_index = bus_index

    def ar(self):
        from supriya.library import audiolib
        assert self.server_session is not None
        if self.calculation_rate == audiolib.CalculationRate.AUDIO:
            result = audiolib.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = audiolib.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = audiolib.K2A.ar(
                source=result,
                )
        return result

    def free(self):
        from supriya.library import audiolib
        ServerObjectProxy.free(self)
        assert self.bus_index is not None
        if self.calculation_rate == audiolib.CalculationRate.AUDIO:
            self.server.audio_bus_allocator.free(self.bus_index)
        else:
            self.server.control_bus_allocator.free(self.bus_index)
        self._bus_index = None

    def kr(self):
        from supriya.library import audiolib
        assert self.server_session is not None
        if self.calculation_rate == audiolib.CalculationRate.CONTROL:
            result = audiolib.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = audiolib.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = audiolib.A2K.ar(
                source=result,
                )
        return result

    def make_set_message(self, *args):
        assert self.is_settable
        assert len(args) <= self.channel_count
        message = ('/c_set',)
        for index, value in enumerate(args):
            index += self.bus_index
            message += (index, value)
        return message

    def set(self, *args):
        assert self.server_session is not None
        message = self.make_set_message(*args)
        self.server.send_message(message)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_index(self):
        return self._bus_index

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def is_settable(self):
        from supriya.library import audiolib
        return self.calculation_rate != audiolib.CalculationRate.AUDIO

    @property
    def map_symbol(self):
        from supriya.library import audiolib
        assert self.bus_index is not None
        if self.calculation_rate == audiolib.CalculationRate.AUDIO:
            string = 'a{}'
        else:
            string = 'c{}'
        string = string.format(self.bus_index)
        return string
