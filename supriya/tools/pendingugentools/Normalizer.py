# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Normalizer(UGen):
    r'''

    ::

        >>> normalizer = ugentools.Normalizer.(
        ...     duration=0.01,
        ...     level=1,
        ...     source=None,
        ...     )
        >>> normalizer

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'level',
        'duration',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        duration=0.01,
        level=1,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            duration=duration,
            level=level,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        duration=0.01,
        level=1,
        source=None,
        ):
        r'''Constructs an audio-rate Normalizer.

        ::

            >>> normalizer = ugentools.Normalizer.ar(
            ...     duration=0.01,
            ...     level=1,
            ...     source=None,
            ...     )
            >>> normalizer

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            duration=duration,
            level=level,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets `duration` input of Normalizer.

        ::

            >>> normalizer = ugentools.Normalizer.ar(
            ...     duration=0.01,
            ...     level=1,
            ...     source=None,
            ...     )
            >>> normalizer.duration

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def level(self):
        r'''Gets `level` input of Normalizer.

        ::

            >>> normalizer = ugentools.Normalizer.ar(
            ...     duration=0.01,
            ...     level=1,
            ...     source=None,
            ...     )
            >>> normalizer.level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Normalizer.

        ::

            >>> normalizer = ugentools.Normalizer.ar(
            ...     duration=0.01,
            ...     level=1,
            ...     source=None,
            ...     )
            >>> normalizer.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]