# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class ExpRand(UGen):
    r'''An exponential random distribution.

    ::

        >>> exp_rand = ugentools.ExpRand.ir()
        >>> exp_rand
        ExpRand.ir()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        minimum=0.,
        maximum=1.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            minimum=minimum,
            maximum=maximum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        maximum=1,
        minimum=0.01,
        ):
        r'''Constructs a scalar-rate exponential random distribution.

        ::

            >>> exp_rand = ugentools.ExpRand.ir(
            ...     maximum=[1.1, 1.2, 1.3],
            ...     minimum=[0.25, 0.75],
            ...     )
            >>> exp_rand
            UGenArray({3})

        returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            )
        return ugen