# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class FreqShift(UGen):
    r'''

    ::

        >>> freq_shift = ugentools.FreqShift.(
        ...     frequency=0,
        ...     phase=0,
        ...     source=None,
        ...     )
        >>> freq_shift

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=0,
        phase=0,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=0,
        phase=0,
        source=None,
        ):
        r'''Constructs an audio-rate FreqShift.

        ::

            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=None,
            ...     )
            >>> freq_shift

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            phase=phase,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of FreqShift.

        ::

            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=None,
            ...     )
            >>> freq_shift.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of FreqShift.

        ::

            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=None,
            ...     )
            >>> freq_shift.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of FreqShift.

        ::

            >>> freq_shift = ugentools.FreqShift.ar(
            ...     frequency=0,
            ...     phase=0,
            ...     source=None,
            ...     )
            >>> freq_shift.phase

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]