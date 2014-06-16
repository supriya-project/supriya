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
        '_bus_id_was_set_manually',
        '_bus_proxies',
        '_channel_count',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        bus_id=None,
        channel_count=1,
        ):
        from supriya.tools import servertools
        ServerObjectProxy.__init__(self)
        channel_count = int(channel_count)
        assert 0 < channel_count
        self._channel_count = channel_count
        assert isinstance(bus_id, (type(None), int))
        self._bus_id = bus_id
        self._bus_id_was_set_manually = False
        if bus_id is not None:
            assert 0 <= bus_id
            self._bus_id_was_set_manually = True
        self._bus_proxies = tuple(
            servertools.BusProxy(bus=self, index=i)
            for i in range(self.channel_count)
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.bus_proxies.__getitem__(item)
        elif isinstance(item, slice):
            indices = item.indices(len(self))
            start = indices[0]
            bus_id = self.bus_id + start
            channel_count = indices[1] - indices[0]
            return type(self)(
                bus_id=bus_id,
                channel_count=channel_count,
                )
        raise TypeError

    def __float__(self):
        return float(self.bus_id)

    def __int__(self):
        return int(self.bus_id)

    def __len__(self):
        return len(self.bus_proxies)

    def __str__(self):
        return self.map_symbol

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
    def is_allocated(self):
        return self.server is not None

    @property
    def map_symbol(self):
        assert self.bus_id is not None
        return Bus._as_map(
            bus_id=self.bus_id,
            calculation_rate=self.calculation_rate,
            )