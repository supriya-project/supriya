# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Osc(PureUGen):
    r'''

    ::

        >>> osc = ugentools.Osc.(
        ...     buffer_id=None,
        ...     frequency=440,
        ...     phase=0,
        ...     )
        >>> osc

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'frequency',
        'phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        r'''Constructs an audio-rate Osc.

        ::

            >>> osc = ugentools.Osc.ar(
            ...     buffer_id=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        r'''Constructs a control-rate Osc.

        ::

            >>> osc = ugentools.Osc.kr(
            ...     buffer_id=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of Osc.

        ::

            >>> osc = ugentools.Osc.ar(
            ...     buffer_id=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of Osc.

        ::

            >>> osc = ugentools.Osc.ar(
            ...     buffer_id=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of Osc.

        ::

            >>> osc = ugentools.Osc.ar(
            ...     buffer_id=None,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc.phase

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]