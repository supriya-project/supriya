# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Decay2(Filter):
    r'''A leaky signal integrator.

    ::

        >>> source = ugentools.Impulse.ar()
        >>> decay_2 = ugentools.Decay2.ar(
        ...     source=source,
        ...     )
        >>> decay_2
        Decay2.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'attack_time',
        'decay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attack_time=0.01,
        decay_time=1.0,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        attack_time=0.01,
        decay_time=1.0,
        source=None,
        ):
        r'''Constructs an audio-rate leaky signal integrator.

        ::

            >>> source = ugentools.Impulse.ar(frequency=[100, 101])
            >>> decay_2 = ugentools.Decay2.ar(
            ...     source=source,
            ...     )
            >>> decay_2
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        attack_time=0.01,
        decay_time=1.0,
        source=None,
        ):
        r'''Constructs a control-rate leaky signal integrator.

        ::

            >>> source = ugentools.Impulse.kr(frequency=[100, 101])
            >>> decay_2 = ugentools.Decay2.kr(
            ...     source=source,
            ...     )
            >>> decay_2
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def attack_time(self):
        r'''Gets `attack_time` input of Decay2.

        ::

            >>> attack_time = 0.5
            >>> decay_time = 0.25
            >>> source = ugentools.In.kr(bus=0)
            >>> decay_2 = ugentools.Decay2.ar(
            ...     attack_time=attack_time,
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay_2.attack_time
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of Decay2.

        ::

            >>> attack_time = 0.5
            >>> decay_time = 0.25
            >>> source = ugentools.In.kr(bus=0)
            >>> decay_2 = ugentools.Decay2.ar(
            ...     attack_time=attack_time,
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay_2.decay_time
            0.25

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Decay2.

        ::

            >>> attack_time = 0.5
            >>> decay_time = 0.25
            >>> source = ugentools.In.kr(bus=0)
            >>> decay_2 = ugentools.Decay2.ar(
            ...     attack_time=attack_time,
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay_2.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    rate=<CalculationRate.CONTROL: 1>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]