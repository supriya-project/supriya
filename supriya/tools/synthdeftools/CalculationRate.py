# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.Enumeration import Enumeration


class CalculationRate(Enumeration):
    r'''An enumeration of scsynth calculation-rates.

    ::

        >>> from supriya.tools import synthdeftools
        >>> synthdeftools.CalculationRate.AUDIO
        <CalculationRate.AUDIO: 2>

    ::

        >>> synthdeftools.CalculationRate.from_expr('demand')
        <CalculationRate.DEMAND: 3>

    '''

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 1
    DEMAND = 3
    SCALAR = 0

    ### PUBLIC METHODS ###

    @staticmethod
    def from_collection(collection):
        r'''Gets calculation-rate from a collection.

        ::

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools

        ::

            >>> collection = []
            >>> collection.append(ugentools.DC.ar(0))
            >>> collection.append(ugentools.DC.kr(1))
            >>> collection.append(2.0)
            >>> synthdeftools.CalculationRate.from_collection(collection)
            <CalculationRate.AUDIO: 2>

        ::
            >>> collection = []
            >>> collection.append(ugentools.DC.kr(1))
            >>> collection.append(2.0)
            >>> synthdeftools.CalculationRate.from_collection(collection)
            <CalculationRate.CONTROL: 1>

        Return calculation-rate.
        '''
        rates = [
            CalculationRate.from_input(item) for item in collection
            ]
        maximum_rate = max(rates)
        return maximum_rate

    @staticmethod
    def from_input(input_):
        from supriya.tools import synthdeftools
        if isinstance(input_, (int, float)):
            return CalculationRate.SCALAR
        elif isinstance(input_, (
            synthdeftools.OutputProxy,
            synthdeftools.UGen,
            )):
            return input_.calculation_rate
        elif isinstance(input_, synthdeftools.Parameter):
            name = input_.parameter_rate.name
            if name == 'TRIGGER':
                return CalculationRate.CONTROL
            return CalculationRate.from_expr(name)
        elif isinstance(input_, collections.Sequence):
            return CalculationRate.from_collection(input_)
        raise ValueError(input_)

    @staticmethod
    def from_ugen_method_mixin(expr):
        if isinstance(expr, collections.Sequence):
            return CalculationRate.from_collection(expr)
        return CalculationRate.from_input(expr)