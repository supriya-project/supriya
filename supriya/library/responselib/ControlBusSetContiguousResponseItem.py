# -*- encoding: utf-8 -*-
from supriya.library.responselib.ServerResponse import ServerResponse


class ControlBusSetContiguousResponseItem(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_values',
        '_starting_bus_index',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        starting_bus_index=None,
        bus_values=None
        ):
        self._bus_values = bus_values
        self._starting_bus_index = starting_bus_index

    ### PUBLIC PROPERTIES ###

    @property
    def bus_values(self):
        return self._bus_values

    @property
    def starting_bus_index(self):
        return self._starting_bus_index
