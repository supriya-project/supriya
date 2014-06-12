# -*- encoding: utf-8 -*-
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy):
    r'''A bus.

    ::

        >>> from supriya import synthdeftools
        >>> from supriya import servertools
        >>> bus = servertools.Bus(
        ...    calculation_rate=synthdeftools.CalculationRate.AUDIO,
        ...    )

    '''
    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_id',
        '_calculation_rate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
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
        self._bus_id = None

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        from supriya.tools import synthdeftools
        ServerObjectProxy.allocate(self, server=server)
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            bus_id = server.audio_bus_allocator.allocate()
        else:
            bus_id = server.control_bus_allocator.allocate()
        if bus_id is None:
            raise Exception
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            assert bus_id not in self._server._audio_busses
            self._server._audio_busses[self._bus_id] = self
        else:
            assert bus_id not in self._server._control_busses
            self._server._control_busses[self._bus_id] = self
        self._bus_id = bus_id

    def ar(self):
        from supriya.tools import synthdeftools
        assert self.server is not None
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            result = synthdeftools.In.ar(bus=self.bus_id)
        else:
            result = synthdeftools.In.kr(bus=self.bus_id)
            result = synthdeftools.K2A.ar(source=result)
        return result

    def free(self):
        from supriya.tools import synthdeftools
        if self.server is not None:
            if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
                self.server.audio_bus_allocator.free(self.bus_id)
                del(self.server._audio_busses[self._bus_id])
            else:
                self.server.control_bus_allocator.free(self.bus_id)
                del(self.server._control_busses[self._bus_id])
        self._bus_id = None
        ServerObjectProxy.free(self)

    def kr(self):
        from supriya.tools import synthdeftools
        assert self.server is not None
        if self.calculation_rate == synthdeftools.CalculationRate.CONTROL:
            result = synthdeftools.In.kr(bus=self.bus_id)
        else:
            result = synthdeftools.In.ar(bus=self.bus_id)
            result = synthdeftools.A2K.ar(source=result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def is_settable(self):
        from supriya.tools import synthdeftools
        return self.calculation_rate != synthdeftools.CalculationRate.AUDIO

    @property
    def map_symbol(self):
        from supriya.tools import synthdeftools
        assert self.bus_id is not None
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            string = 'a{}'
        else:
            string = 'c{}'
        string = string.format(self.bus_id)
        return string
