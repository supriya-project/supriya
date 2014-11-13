# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class TExpRand(UGen):
    r'''A triggered exponential random number generator.

    ::

        >>> trigger = ugentools.Impulse.ar()
        >>> t_exp_rand = ugentools.TExpRand.ar(
        ...     minimum=-1.,
        ...     maximum=1.,
        ...     trigger=trigger,
        ...     )
        >>> t_exp_rand
        TExpRand.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        maximum=1,
        minimum=0.01,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        maximum=1,
        minimum=0.01,
        trigger=0,
        ):
        r'''Constructs an audio-rate triggered exponential random number
        generator.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_exp_rand = ugentools.TExpRand.ar(
            ...     minimum=0,
            ...     maximum=[1., 2.],
            ...     trigger=trigger,
            ...     )
            >>> t_exp_rand
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        maximum=1,
        minimum=0.01,
        trigger=0,
        ):
        r'''Constructs a control-rate triggered exponential random number
        generator.

        ::

            >>> trigger = ugentools.Impulse.kr()
            >>> t_exp_rand = ugentools.TExpRand.kr(
            ...     minimum=0,
            ...     maximum=[1., 2.],
            ...     trigger=trigger,
            ...     )
            >>> t_exp_rand
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            trigger=trigger,
            )
        return ugen