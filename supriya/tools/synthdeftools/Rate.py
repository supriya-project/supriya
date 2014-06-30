# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class Rate(Enumeration):
    r'''An enumeration of scsynth calculation rates.

    ::

        >>> from supriya.tools import synthdeftools
        >>> synthdeftools.Rate.AUDIO
        <Rate.AUDIO: 2>

    ::

        >>> synthdeftools.Rate.from_expr('demand')
        <Rate.DEMAND: 3>

    '''

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 1
    DEMAND = 3
    SCALAR = 0

    ### PUBLIC METHODS ###

    @staticmethod
    def from_collection(collection):
        r'''Gets calculation rate from a collection.

        ::

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools

        ::

            >>> collection = []
            >>> collection.append(ugentools.DC.ar(0))
            >>> collection.append(ugentools.DC.kr(1))
            >>> collection.append(2.0)
            >>> synthdeftools.Rate.from_collection(collection)
            <Rate.AUDIO: 2>

        ::
            >>> collection = []
            >>> collection.append(ugentools.DC.kr(1))
            >>> collection.append(2.0)
            >>> synthdeftools.Rate.from_collection(collection)
            <Rate.CONTROL: 1>

        Return calculation rate.
        '''
        rates = [
            Rate.from_input(item) for item in collection
            ]
        maximum_rate = max(rates)
        return maximum_rate

    @staticmethod
    def from_input(input_):
        from supriya.tools import synthdeftools
        if isinstance(input_, (int, float)):
            return Rate.SCALAR
        elif isinstance(input_, (
            synthdeftools.OutputProxy, synthdeftools.UGen)):
            return input_.rate
        elif isinstance(input_, synthdeftools.Parameter):
            name = input_.parameter_rate.name
            if name == 'TRIGGER':
                return Rate.CONTROL
            return Rate.from_expr(name)
        raise ValueError(input_)
