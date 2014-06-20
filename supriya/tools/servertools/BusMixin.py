# -*- encoding: utf-8 -*-
import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BusMixin(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.bus_id)

    def __int__(self):
        return int(self.bus_id)

    def __str__(self):
        return self.map_symbol

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def bus_id(self):
        return self._bus_id
        raise NotImplementedError

    @abc.abstractproperty
    def calculation_rate(self):
        raise NotImplementedError

    @property
    def map_symbol(self):
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
        map_symbol += str(self.bus_id)
        return map_symbol
