# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class TIRand(UGen):
    r'''A triggered integer random number generator.

    ::

        >>> trigger = ugentools.Impulse.ar()
        >>> t_i_rand = ugentools.TIRand.ar(
        ...     minimum=0,
        ...     maximum=127,
        ...     trigger=trigger,
        ...     )
        >>> t_i_rand
        TIRand.ar()

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
        maximum=127,
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
        maximum=127,
        minimum=0,
        trigger=0,
        ):
        r'''Constructs an audio-rate triggered integer random number generator.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_i_rand = ugentools.TIRand.ar(
            ...     minimum=0,
            ...     maximum=[64, 127],
            ...     trigger=trigger,
            ...     )
            >>> t_i_rand
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
        maximum=127,
        minimum=0,
        trigger=0,
        ):
        r'''Constructs a control-rate triggered integer random number generator.

        ::

            >>> trigger = ugentools.Impulse.kr()
            >>> t_i_rand = ugentools.TIRand.kr(
            ...     minimum=0,
            ...     maximum=[64, 127],
            ...     trigger=trigger,
            ...     )
            >>> t_i_rand
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

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        r'''Gets `maximum` input of TIRand.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_i_rand = ugentools.TIRand.ar(
            ...     minimum=0,
            ...     maximum=127,
            ...     trigger=trigger,
            ...     )
            >>> t_i_rand.maximum
            127.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        r'''Gets `minimum` input of TIRand.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_i_rand = ugentools.TIRand.ar(
            ...     minimum=0,
            ...     maximum=127,
            ...     trigger=trigger,
            ...     )
            >>> t_i_rand.minimum
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of TIRand.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_i_rand = ugentools.TIRand.ar(
            ...     minimum=0,
            ...     maximum=127,
            ...     trigger=trigger,
            ...     )
            >>> t_i_rand.trigger
            OutputProxy(
                source=Impulse(
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )


        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]