# -*- encoding: utf-8 -*-
import collections
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy, collections.Sequence):
    r'''A bus.

    ::

        >>> from supriya import synthdeftools
        >>> from supriya import servertools
        >>> bus = servertools.Bus(
        ...    calculation_rate=synthdeftools.CalculationRate.AUDIO,
        ...    )

    ::

        >>> server = servertools.Server().boot()
        >>> bus.allocate()
        >>> bus[0]
        BusProxy(
            bus=Bus(
                calculation_rate=<CalculationRate.AUDIO: 2>,
                channel_count=1
                ),
            index=0
            )

    ::

        >>> bus[0].map_symbol
        'a0'

    ::

        >>> bus.free()
        >>> server = server.quit()
        RECV: OscMessage('/done', '/quit')

    '''
    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_id',
        '_bus_proxies',
        '_calculation_rate',
        '_channel_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=1,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        if calculation_rate is None:
            calculation_rate = synthdeftools.CalculationRate.AUDIO
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        assert calculation_rate in (
            synthdeftools.CalculationRate.AUDIO,
            synthdeftools.CalculationRate.CONTROL,
            )
        channel_count = int(channel_count)
        assert 0 < channel_count
        self._calculation_rate = calculation_rate
        self._channel_count = channel_count
        self._bus_id = None
        self._bus_proxies = tuple(
            servertools.BusProxy(bus=self, index=i)
            for i in range(self.channel_count)
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self.bus_proxies.__getitem__(item)

    def __len__(self):
        return len(self.bus_proxies)

    ### PRIVATE METHODS ###

    @staticmethod
    def _as_map(
        bus_id=None,
        calculation_rate=None,
        ):
        from supriya.tools import synthdeftools
        if calculation_rate == synthdeftools.CalculationRate.AUDIO:
            string = 'a{}'
        elif calculation_rate == synthdeftools.CalculationRate.CONTROL:
            string = 'c{}'
        else:
            raise ValueError
        string = string.format(bus_id)
        return string

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        from supriya.tools import synthdeftools
        ServerObjectProxy.allocate(self, server=server)
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            bus_id = self.server.audio_bus_allocator.allocate()
        else:
            bus_id = self.server.control_bus_allocator.allocate()
        if bus_id is None:
            raise Exception
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            assert bus_id not in self.server._audio_busses
            self.server._audio_busses[bus_id] = self
        else:
            assert bus_id not in self.server._control_busses
            self.server._control_busses[bus_id] = self
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
    def bus_proxies(self):
        return self._bus_proxies

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
        assert self.bus_id is not None
        return Bus._as_map(
            bus_id=self.bus_id,
            calculation_rate=self.calculation_rate,
            )
