# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Amplitude(UGen):
    r'''

    ::

        >>> amplitude = ugentools.Amplitude.(
        ...     attack_time=0.01,
        ...     release_time=0.01,
        ...     source=None,
        ...     )
        >>> amplitude

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'attack_time',
        'release_time',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        attack_time=0.01,
        release_time=0.01,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            release_time=release_time,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        attack_time=0.01,
        release_time=0.01,
        source=None,
        ):
        r'''Constructs an audio-rate Amplitude.

        ::

            >>> amplitude = ugentools.Amplitude.ar(
            ...     attack_time=0.01,
            ...     release_time=0.01,
            ...     source=None,
            ...     )
            >>> amplitude

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            release_time=release_time,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        attack_time=0.01,
        release_time=0.01,
        source=None,
        ):
        r'''Constructs a control-rate Amplitude.

        ::

            >>> amplitude = ugentools.Amplitude.kr(
            ...     attack_time=0.01,
            ...     release_time=0.01,
            ...     source=None,
            ...     )
            >>> amplitude

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            release_time=release_time,
            source=source,
            )
        return ugen

    @classmethod
    def new(
        cls,
        source=None,
        ):
        r'''Constructs a Amplitude.

        ::

            >>> amplitude = ugentools.Amplitude.new(
            ...     source=None,
            ...     )
            >>> amplitude

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Amplitude.

        ::

            >>> amplitude = ugentools.Amplitude.ar(
            ...     attack_time=0.01,
            ...     release_time=0.01,
            ...     source=None,
            ...     )
            >>> amplitude.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def attack_time(self):
        r'''Gets `attack_time` input of Amplitude.

        ::

            >>> amplitude = ugentools.Amplitude.ar(
            ...     attack_time=0.01,
            ...     release_time=0.01,
            ...     source=None,
            ...     )
            >>> amplitude.attack_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def release_time(self):
        r'''Gets `release_time` input of Amplitude.

        ::

            >>> amplitude = ugentools.Amplitude.ar(
            ...     attack_time=0.01,
            ...     release_time=0.01,
            ...     source=None,
            ...     )
            >>> amplitude.release_time

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('release_time')
        return self._inputs[index]