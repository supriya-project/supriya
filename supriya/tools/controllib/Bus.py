# -*- encoding: utf-8 -*-
from supriya.tools.controllib.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy):
    r'''A bus.

    ::

        >>> from supriya import synthdefinitiontools
        >>> from supriya import controllib
        >>> bus = controllib.Bus(
        ...    calculation_rate=synthdefinitiontools.CalculationRate.AUDIO,
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
        from supriya.tools import synthdefinitiontools
        ServerObjectProxy.__init__(self)
        if calculation_rate is None:
            calculation_rate = synthdefinitiontools.CalculationRate.AUDIO
        calculation_rate = synthdefinitiontools.CalculationRate.from_expr(calculation_rate)
        assert calculation_rate in (
            synthdefinitiontools.CalculationRate.AUDIO,
            synthdefinitiontools.CalculationRate.CONTROL,
            )
        self._calculation_rate = calculation_rate
        self._channel_count = int(channel_count)
        self._bus_index = None

    ### PUBLIC METHODS ###

    def allocate(self, server_session=None):
        from supriya.tools import synthdefinitiontools
        ServerObjectProxy.allocate(self)
        channel_count = self.channel_count
        if self.calculation_rate == synthdefinitiontools.CalculationRate.AUDIO:
            bus_index = server_session.audio_bus_allocator.allocate(
                channel_count)
        else:
            bus_index = server_session.control_bus_allocator.allocate(
                channel_count)
        if bus_index is None:
            raise Exception
        self._bus_index = bus_index

    def ar(self):
        from supriya.tools import synthdefinitiontools
        assert self.server_session is not None
        if self.calculation_rate == synthdefinitiontools.CalculationRate.AUDIO:
            result = synthdefinitiontools.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = synthdefinitiontools.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = synthdefinitiontools.K2A.ar(
                source=result,
                )
        return result

    def free(self):
        from supriya.tools import synthdefinitiontools
        ServerObjectProxy.free(self)
        assert self.bus_index is not None
        if self.calculation_rate == synthdefinitiontools.CalculationRate.AUDIO:
            self.server.audio_bus_allocator.free(self.bus_index)
        else:
            self.server.control_bus_allocator.free(self.bus_index)
        self._bus_index = None

    def kr(self):
        from supriya.tools import synthdefinitiontools
        assert self.server_session is not None
        if self.calculation_rate == synthdefinitiontools.CalculationRate.CONTROL:
            result = synthdefinitiontools.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = synthdefinitiontools.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = synthdefinitiontools.A2K.ar(
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
        from supriya.tools import synthdefinitiontools
        return self.calculation_rate != synthdefinitiontools.CalculationRate.AUDIO

    @property
    def map_symbol(self):
        from supriya.tools import synthdefinitiontools
        assert self.bus_index is not None
        if self.calculation_rate == synthdefinitiontools.CalculationRate.AUDIO:
            string = 'a{}'
        else:
            string = 'c{}'
        string = string.format(self.bus_index)
        return string
