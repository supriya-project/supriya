# -*- encoding: utf-8 -*-
from supriya.tools.servertools.BusMixin import BusMixin
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy, BusMixin):
    r'''A bus.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_group',
        '_bus_id',
        '_bus_id_was_set_manually',
        '_calculation_rate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_group_or_index=None,
        calculation_rate=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        bus_group = None
        bus_id = None
        self._bus_id_was_set_manually = False
        if bus_group_or_index is not None:
            self._bus_id_was_set_manually = True
            if isinstance(bus_group_or_index, servertools.BusGroup):
                bus_group = bus_group_or_index
            elif isinstance(bus_group_or_index, int):
                bus_id = int(bus_group_or_index)
        self._bus_group = bus_group
        self._bus_id = bus_id
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        self._calculation_rate = calculation_rate

    ### SPECIAL METHODS ###

    def __repr__(self):
        string = '<{}: {}>'.format(
            type(self).__name__,
            self.bus_id,
            )
        return string

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_allocator(
        calculation_rate=None,
        server=None,
        ):
        from supriya.tools import synthdeftools
        if calculation_rate == synthdeftools.CalculationRate.AUDIO:
            allocator = server.audio_bus_allocator
        else:
            allocator = server.control_bus_allocator
        return allocator

    ### PUBLIC METHODS ###

    def allocate(
        self,
        server=None,
        ):
        if self.bus_group is not None:
            return
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(self, server=server)
        if self.bus_id is None:
            allocator = self._get_allocator(
                calculation_rate=self.calculation_rate,
                server=self.server,
                )
            bus_id = allocator.allocate(1)
            if bus_id is None:
                ServerObjectProxy.free(self)
                raise ValueError
            self._bus_id = bus_id

    def free(self):
        if not self.is_allocated:
            return
        if not self._bus_id_was_set_manually:
            allocator = self._get_allocator(
                calculation_rate=self.calculation_rate,
                server=self.server,
                )
            allocator.free(self.bus_id)
        self._bus_id = None
        ServerObjectProxy.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self):
        return self._bus_group

    @property
    def bus_id(self):
        if self._bus_group is not None:
            if self._bus_group.bus_id is not None:
                group_id = self._bus_group.bus_id
                index = self._bus_group.index(self)
                bus_id = group_id + index
                return bus_id
        return self._bus_id

    @property
    def is_allocated(self):
        if self.bus_group is not None:
            return self.bus_group.is_allocated
        return self.server is not None

    @property
    def server(self):
        if self.bus_group is not None:
            return self.bus_group.server
        return self._server

    @property
    def value(self):
        from supriya.tools import synthdeftools
        if self.is_allocated:
            if self.calculation_rate == synthdeftools.CalculationRate.CONTROL:
                proxy = self.server._get_control_bus_proxy(self.bus_id)
                return proxy.value
        return None
