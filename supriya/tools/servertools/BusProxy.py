# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BusProxy(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus',
        '_index',
        )

    ### INITIALIZER ###

    def __init__(self,
        bus=None,
        index=None,
        ):
        from supriya.tools import servertools
        assert isinstance(bus, servertools.Bus)
        index = int(index)
        assert 0 <= index <= bus.channel_count
        self._bus = bus
        self._index = index

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __float__(self):
        return float(self.bus_id)

    def __hash__(self):
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    def __int__(self):
        return int(self.bus_id)

    def __str__(self):
        return self.map_symbol

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        return self._bus

    @property
    def bus_id(self):
        if self.bus.bus_id is None:
            return None
        return self.bus.bus_id + self.index

    @property
    def calculation_rate(self):
        return self.bus.calculation_rate

    @property
    def index(self):
        return self._index

    @property
    def map_symbol(self):
        from supriya.tools import servertools
        assert self.bus_id is not None
        return servertools.Bus._as_map(
            bus_id=self.bus_id,
            calculation_rate=self.calculation_rate,
            )
