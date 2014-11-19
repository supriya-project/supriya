# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class VOsc(PureUGen):
    r'''

    ::

        >>> vosc = ugentools.VOsc.(
        ...     bufpos=None,
        ...     frequency=440,
        ...     phase=0,
        ...     )
        >>> vosc

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'bufpos',
        'frequency',
        'phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bufpos=None,
        frequency=440,
        phase=0,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            frequency=frequency,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufpos=None,
        frequency=440,
        phase=0,
        ):
        r'''Constructs an audio-rate VOsc.

        ::

            >>> vosc = ugentools.VOsc.ar(
            ...     bufpos=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bufpos=None,
        frequency=440,
        phase=0,
        ):
        r'''Constructs a control-rate VOsc.

        ::

            >>> vosc = ugentools.VOsc.kr(
            ...     bufpos=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bufpos(self):
        r'''Gets `bufpos` input of VOsc.

        ::

            >>> vosc = ugentools.VOsc.ar(
            ...     bufpos=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc.bufpos

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bufpos')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of VOsc.

        ::

            >>> vosc = ugentools.VOsc.ar(
            ...     bufpos=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of VOsc.

        ::

            >>> vosc = ugentools.VOsc.ar(
            ...     bufpos=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> vosc.phase

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]