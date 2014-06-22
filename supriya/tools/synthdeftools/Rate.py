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

        ::

            >>> collection = []
            >>> collection.append(synthdeftools.DC.ar(0))
            >>> collection.append(synthdeftools.DC.kr(1))
            >>> collection.append(2.0)
            >>> synthdeftools.Rate.from_collection(collection)
            <Rate.AUDIO: 2>

        ::
            >>> collection = []
            >>> collection.append(synthdeftools.DC.kr(1))
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
        prototype = (synthdeftools.OutputProxy, synthdeftools.UGen)
        if isinstance(input_, (int, float)):
            return Rate.SCALAR
        elif isinstance(input_, prototype):
            return input_.rate
        raise ValueError(input_)

