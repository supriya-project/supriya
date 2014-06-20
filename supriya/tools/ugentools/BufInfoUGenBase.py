# -*- encoding: utf-8 -*-
import abc
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class BufInfoUGenBase(InfoUGenBase):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'buffer_number',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        buffer_number=None,
        calculation_rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            buffer_number=buffer_number,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, buffer_number=None):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            buffer_number=buffer_number,
            calculation_rate=calculation_rate,
            )
        return ugen

    @classmethod
    def kr(cls, buffer_number=None):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            buffer_number=buffer_number,
            calculation_rate=calculation_rate,
            )
        return ugen
