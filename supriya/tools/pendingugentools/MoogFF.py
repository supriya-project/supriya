# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class MoogFF(Filter):
    r'''

    ::

        >>> moog_ff = ugentools.MoogFF.ar(
        ...     frequency=100,
        ...     gain=2,
        ...     reset=0,
        ...     source=source,
        ...     )
        >>> moog_ff
        MoogFF.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'gain',
        'reset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=100,
        gain=2,
        reset=0,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=100,
        gain=2,
        reset=0,
        source=source,
        ):
        r'''Constructs an audio-rate MoogFF.

        ::

            >>> moog_ff = ugentools.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff
            MoogFF.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        frequency=100,
        gain=2,
        reset=0,
        source=source,
        ):
        r'''Constructs a control-rate MoogFF.

        ::

            >>> moog_ff = ugentools.MoogFF.kr(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff
            MoogFF.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            gain=gain,
            reset=reset,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of MoogFF.

        ::

            >>> moog_ff = ugentools.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.frequency
            100.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def gain(self):
        r'''Gets `gain` input of MoogFF.

        ::

            >>> moog_ff = ugentools.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.gain
            2.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def reset(self):
        r'''Gets `reset` input of MoogFF.

        ::

            >>> moog_ff = ugentools.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.reset
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of MoogFF.

        ::

            >>> moog_ff = ugentools.MoogFF.ar(
            ...     frequency=100,
            ...     gain=2,
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> moog_ff.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]