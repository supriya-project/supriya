# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class TDelay(UGen):
    r'''A trigger delay.

    ::

        >>> source = ugentools.Dust.kr()
        >>> tdelay = ugentools.TDelay.ar(
        ...     duration=0.1,
        ...     source=source,
        ...     )
        >>> tdelay
        TDelay.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'duration',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        duration=0.1,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            duration=duration,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        duration=0.1,
        source=None,
        ):
        r'''Constructs an audio-rate TDelay.

        ::

            >>> source = ugentools.Dust.kr()
            >>> tdelay = ugentools.TDelay.ar(
            ...     duration=0.1,
            ...     source=source,
            ...     )
            >>> tdelay
            TDelay.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            duration=duration,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        duration=0.1,
        source=None,
        ):
        r'''Constructs a control-rate TDelay.

        ::

            >>> source = ugentools.Dust.kr()
            >>> tdelay = ugentools.TDelay.kr(
            ...     duration=0.1,
            ...     source=source,
            ...     )
            >>> tdelay
            TDelay.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            duration=duration,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets `duration` input of TDelay.

        ::

            >>> source = ugentools.Dust.kr()
            >>> tdelay = ugentools.TDelay.ar(
            ...     duration=0.1,
            ...     source=source,
            ...     )
            >>> tdelay.duration
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of TDelay.

        ::

            >>> source = ugentools.Dust.kr()
            >>> tdelay = ugentools.TDelay.ar(
            ...     duration=0.1,
            ...     source=source,
            ...     )
            >>> tdelay.source
            OutputProxy(
                source=Dust(
                    calculation_rate=CalculationRate.CONTROL,
                    density=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]