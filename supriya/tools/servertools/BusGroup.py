# -*- encoding: utf-8 -*-
import collections
from supriya.tools.servertools.BusMixin import BusMixin
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class BusGroup(ServerObjectProxy, BusMixin, collections.Sequence):
    r'''A bus group.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_id',
        '_buses',
        '_calculation_rate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_count=1,
        calculation_rate=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        self._bus_id = None
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        self._calculation_rate = calculation_rate
        bus_count = int(bus_count)
        assert 0 < bus_count
        self._buses = tuple(
            servertools.Bus(
                bus_group_or_index=self,
                calculation_rate=self.calculation_rate,
                )
            for _ in range(bus_count)
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._buses[item]

    def __len__(self):
        return len(self._buses)

    def __repr__(self):
        string = '<{}: {{{}}} @ {}>'.format(
            type(self).__name__,
            len(self),
            self.bus_id
            )
        return string

    ### PUBLIC METHODS ###

    def allocate(
        self,
        server=None,
        ):
        from supriya.tools import servertools
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(self, server=server)
        allocator = servertools.Bus._get_allocator(
            calculation_rate=self.calculation_rate,
            server=self.server,
            )
        bus_id = allocator.allocate(len(self))
        if bus_id is None:
            ServerObjectProxy.free(self)
            raise ValueError
        self._bus_id = bus_id

    def free(self):
        from supriya.tools import servertools
        if not self.is_allocated:
            return
        allocator = servertools.Bus._get_allocator(
            calculation_rate=self.calculation_rate,
            server=self.server,
            )
        allocator.free(self.bus_id)
        self._bus_id = None
        ServerObjectProxy.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def buses(self):
        return self._buses

    @property
    def is_allocated(self):
        return self.server is not None
