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

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        r'''Gets `maximum` input of TRand.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_rand = ugentools.TRand.ar(
            ...     minimum=-1.,
            ...     maximum=1.,
            ...     trigger=trigger,
            ...     )
            >>> t_rand.maximum
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        r'''Gets `minimum` input of TRand.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_rand = ugentools.TRand.ar(
            ...     minimum=-1.,
            ...     maximum=1.,
            ...     trigger=trigger,
            ...     )
            >>> t_rand.minimum
            -1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of TRand.

        ::

            >>> trigger = ugentools.Impulse.ar()
            >>> t_rand = ugentools.TRand.ar(
            ...     minimum=-1.,
            ...     maximum=1.,
            ...     trigger=trigger,
            ...     )
            >>> t_rand.trigger
            OutputProxy(
                source=Impulse(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )


        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]