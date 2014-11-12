# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class LinRand(UGen):
    r'''A skewed linear random distribution.

    ::

        >>> lin_rand = ugentools.LinRand.ir(
        ...    minimum=-1.,
        ...    maximum=1.,
        ...    skew=0.5,
        ...    )
        >>> lin_rand
        LinRand.ir()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'skew',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        minimum=0.,
        maximum=1.,
        skew=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            minimum=minimum,
            maximum=maximum,
            skew=skew,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        maximum=1,
        minimum=0,
        skew=0,
        ):
        r'''Constructs a skewed linear random distribution.

        ::

            >>> lin_rand = ugentools.LinRand.ir(
            ...    minimum=-1.,
            ...    maximum=1.,
            ...    skew=[-0.5, 0.5],
            ...    )
            >>> lin_rand
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            skew=skew,
            )
        return ugen