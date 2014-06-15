# -*- encoding: utf-8 -*-
import abc
import collections
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy, collections.Sequence):
    r'''Abstract parent class for busses.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_id',
        '_bus_proxies',
        '_channel_count',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        channel_count=1,
        ):
        from supriya.tools import servertools
        ServerObjectProxy.__init__(self)
        channel_count = int(channel_count)
        assert 0 < channel_count
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

    def ar(self):
        from supriya.tools import synthdeftools
        assert self.server is not None
        bus_ids = [x.bus_id for x in self]
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            result = synthdeftools.In.ar(bus=bus_ids)
        else:
            result = synthdeftools.In.kr(bus=bus_ids)
            result = synthdeftools.K2A.ar(source=result)
        return result

    def kr(self):
        from supriya.tools import synthdeftools
        assert self.server is not None
        bus_ids = [x.bus_id for x in self]
        if self.calculation_rate == synthdeftools.CalculationRate.CONTROL:
            result = synthdeftools.In.kr(bus=bus_ids)
        else:
            result = synthdeftools.In.ar(bus=bus_ids)
            result = synthdeftools.A2K.ar(source=result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def bus_proxies(self):
        return self._bus_proxies

    @abc.abstractproperty
    def calculation_rate(self):
        raise NotImplementedError

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def map_symbol(self):
        assert self.bus_id is not None
        return Bus._as_map(
            bus_id=self.bus_id,
            calculation_rate=self.calculation_rate,
            )
