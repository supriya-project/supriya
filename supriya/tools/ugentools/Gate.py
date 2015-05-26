# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Gate(UGen):
    r'''Gates or holds.

    ::

        >>> source = ugentools.WhiteNoise.ar()
        >>> trigger = ugentools.Dust.kr(1)
        >>> gate = ugentools.Gate.ar(
        ...     source=source,
        ...     trigger=trigger,
        ...     )
        >>> gate
        Gate.ar()

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
        r'''Constructs an audio-rate Gate.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> gate = ugentools.Gate.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate
            Gate.ar()

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
        r'''Constructs a control-rate Gate.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> gate = ugentools.Gate.kr(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate
            Gate.kr()

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
        r'''Gets `source` input of Gate.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> gate = ugentools.Gate.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate.source
            OutputProxy(
                source=WhiteNoise(
                    calculation_rate=CalculationRate.AUDIO
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Gate.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> trigger = ugentools.Dust.kr(1)
            >>> gate = ugentools.Gate.ar(
            ...     source=source,
            ...     trigger=trigger,
            ...     )
            >>> gate.trigger
            OutputProxy(
                source=Dust(
                    calculation_rate=CalculationRate.CONTROL,
                    density=1.0
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]