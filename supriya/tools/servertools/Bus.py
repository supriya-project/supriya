# -*- encoding: utf-8 -*-
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy):
    r'''A bus.

    ::

        >>> from supriya import synthdeftools
        >>> from supriya import servertools
        >>> bus = servertools.Bus(
        ...    calculation_rate=synthdeftools.CalculationRate.AUDIO,
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
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        if calculation_rate is None:
            calculation_rate = synthdeftools.CalculationRate.AUDIO
        calculation_rate = synthdeftools.CalculationRate.from_expr(calculation_rate)
        assert calculation_rate in (
            synthdeftools.CalculationRate.AUDIO,
            synthdeftools.CalculationRate.CONTROL,
            )
        self._calculation_rate = calculation_rate
        self._channel_count = int(channel_count)
        self._bus_index = None

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        from supriya.tools import synthdeftools
        ServerObjectProxy.allocate(self, server=server)
        channel_count = self.channel_count
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            bus_index = server.audio_bus_allocator.allocate(
                channel_count)
        else:
            bus_index = server.control_bus_allocator.allocate(
                channel_count)
        if bus_index is None:
            raise Exception
        self._bus_index = bus_index

    def ar(self):
        from supriya.tools import synthdeftools
        assert self.server is not None
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            result = synthdeftools.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = synthdeftools.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = synthdeftools.K2A.ar(
                source=result,
                )
        return result

    def free(self):
        from supriya.tools import synthdeftools
        ServerObjectProxy.free(self)
        assert self.bus_index is not None
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            self.server.audio_bus_allocator.free(self.bus_index)
        else:
            self.server.control_bus_allocator.free(self.bus_index)
        self._bus_index = None

    def kr(self):
        from supriya.tools import synthdeftools
        assert self.server is not None
        if self.calculation_rate == synthdeftools.CalculationRate.CONTROL:
            result = synthdeftools.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = synthdeftools.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = synthdeftools.A2K.ar(
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
        assert self.server is not None
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
        from supriya.tools import synthdeftools
        return self.calculation_rate != synthdeftools.CalculationRate.AUDIO

    @property
    def map_symbol(self):
        from supriya.tools import synthdeftools
        assert self.bus_index is not None
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            string = 'a{}'
        else:
            string = 'c{}'
        string = string.format(self.bus_index)
        return string
