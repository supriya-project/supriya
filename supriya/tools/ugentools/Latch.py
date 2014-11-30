# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Latch(UGen):
    r'''Samples and holds.

    ::

        >>> source = ugentools.WhiteNoise.ar()
        >>> trigger = ugentools.Dust.kr(1)
        >>> latch = ugentools.Latch.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> latch
        Latch.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        trigger=0,
        ):
        r'''Constructs an audio-rate Latch.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> latch = ugentools.Latch.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> latch
            Latch.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        trigger=0,
        ):
        r'''Constructs a control-rate Latch.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> latch = ugentools.Latch.kr(
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> latch
            Latch.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Latch.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> latch = ugentools.Latch.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> latch.source
            OutputProxy(
                source=WhiteNoise(
                    calculation_rate=<CalculationRate.AUDIO: 2>
                    ),
                output_index=0
                )


        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Latch.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> latch = ugentools.Latch.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> latch.trigger
            OutputProxy(
                source=Dust(
                    calculation_rate=<CalculationRate.CONTROL: 1>,
                    density=1.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]