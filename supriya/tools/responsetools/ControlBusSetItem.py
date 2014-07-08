# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class ControlBusSetItem(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_id',
        '_bus_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_id=None,
        bus_value=None,
        ):
        self._bus_id = bus_id
        self._bus_value = bus_value

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def bus_value(self):
        return self._bus_value