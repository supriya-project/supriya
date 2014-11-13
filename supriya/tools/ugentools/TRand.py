# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class TRand(UGen):
    r'''A triggered random number generator.

    ::

        >>> trigger = ugentools.Impulse.ar()
        >>> t_rand = ugentools.TRand.ar(
        ...     minimum=-1.,
        ...     maximum=1.,
        ...     trigger=trigger,
        ...     )
        >>> t_rand
        TRand.ar()

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
        minimum=0,
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
        minimum=0,
        trigger=0,
        ):
        r'''Constructs an audio-rate triggered random number generator.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_rand = ugentools.TRand.ar(
            ...     minimum=-1.,
            ...     maximum=[0, 2],
            ...     trigger=trigger,
            ...     )
            >>> t_rand
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
        minimum=0,
        trigger=0,
        ):
        r'''Constructs a control-rate triggered random number generator.

        ::

            >>> trigger = ugentools.Impulse.kr()
            >>> t_rand = ugentools.TRand.kr(
            ...     minimum=-1.,
            ...     maximum=[0, 2],
            ...     trigger=trigger,
            ...     )
            >>> t_rand
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