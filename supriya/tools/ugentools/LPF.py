# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class LPF(Filter):
    r'''Lowpass filter unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.LPF.ar(source=source)
        LPF.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        )

    ### PUBLIC METHODS ###

    def __init__(
        self,
        frequency=440,
        calculation_rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            frequency=frequency,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        source=None,
        ):
        r'''Creates an audio-rate lowpass filter.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.LPF.ar(
            ...     frequency=440,
            ...     source=source,
            ...     )
            LPF.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        source=None,
        ):
        r'''Creates a control-rate lowpass filter.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.LPF.kr(
            ...     frequency=440,
            ...     source=source,
            ...     )
            LPF.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        r'''Gets `frequency` input of LPF.

        ::

            >>> frequency = 442
            >>> source = ugentools.In.ar(bus=0)
            >>> lpf = ugentools.LPF.ar(
            ...     frequency=frequency,
            ...     source=source,
            ...     )
            >>> lpf.frequency
            442.0

        Returns input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of LPF.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lpf = ugentools.LPF.ar(
            ...     source=source,
            ...     )
            >>> lpf.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]