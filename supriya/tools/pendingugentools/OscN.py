# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class OscN(PureUGen):
    r'''

    ::

        >>> osc_n = ugentools.OscN.ar(
        ...     buffer_id=buffer_id,
        ...     frequency=440,
        ...     phase=0,
        ...     )
        >>> osc_n
        OscN.ar()

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
        r'''Constructs an audio-rate OscN.

        ::

            >>> osc_n = ugentools.OscN.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc_n
            OscN.ar()

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
        r'''Constructs a control-rate OscN.

        ::

            >>> osc_n = ugentools.OscN.kr(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc_n
            OscN.kr()

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
        r'''Gets `buffer_id` input of OscN.

        ::

            >>> osc_n = ugentools.OscN.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc_n.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of OscN.

        ::

            >>> osc_n = ugentools.OscN.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc_n.frequency
            440.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        r'''Gets `phase` input of OscN.

        ::

            >>> osc_n = ugentools.OscN.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc_n.phase
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]