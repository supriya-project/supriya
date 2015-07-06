# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class ZeroCrossing(UGen):
    r'''A zero-crossing frequency follower.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> zero_crossing = ugentools.ZeroCrossing.ar(
        ...     source=source,
        ...     )
        >>> zero_crossing
        ZeroCrossing.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Analysis UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        r'''Constructs an audio-rate ZeroCrossing.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> zero_crossing = ugentools.ZeroCrossing.ar(
            ...     source=source,
            ...     )
            >>> zero_crossing
            ZeroCrossing.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        r'''Constructs a control-rate ZeroCrossing.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> zero_crossing = ugentools.ZeroCrossing.kr(
            ...     source=source,
            ...     )
            >>> zero_crossing
            ZeroCrossing.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of ZeroCrossing.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> zero_crossing = ugentools.ZeroCrossing.ar(
            ...     source=source,
            ...     )
            >>> zero_crossing.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]