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
        bus_id=None,
        rate=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        rate = synthdeftools.Rate.from_expr(
            rate)
        self._calculation_rate = rate
        bus_count = int(bus_count)
        assert 0 < bus_count
        self._buses = tuple(
            servertools.Bus(
                bus_group_or_index=self,
                rate=self.rate,
                )
            for _ in range(bus_count)
            )
        assert isinstance(bus_id, (type(None), int))
        self._bus_id = bus_id

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._buses[item]
        elif isinstance(item, slice):
            indices = item.indices(len(self))
            bus_count = indices[1] - indices[0]
            bus_group = BusGroup(
                bus_count=bus_count,
                bus_id=self.bus_id,
                rate=self.rate,
                )
            return bus_group

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
        sync=False,
        ):
        from supriya.tools import servertools
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(self, server=server)
        allocator = servertools.Bus._get_allocator(
            rate=self.rate,
            server=self.server,
            )
        bus_id = allocator.allocate(len(self))
        if bus_id is None:
            ServerObjectProxy.free(self)
            raise ValueError
        self._bus_id = bus_id
        if sync:
            self.server.sync()
        return self

    def free(self):
        from supriya.tools import servertools
        if not self.is_allocated:
            return
        allocator = servertools.Bus._get_allocator(
            rate=self.rate,
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
    def rate(self):
        return self._calculation_rate

    @property
    def is_allocated(self):
        return self.server is not None
