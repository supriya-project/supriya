# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Delay1(PureUGen):
    """
    A one-sample delay line unit generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.Delay1.ar(source=source)
        Delay1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Delay UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        PureUGen.__init__(
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
        """
        Constructs an audio-rate one-sample delay line.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.Delay1.ar(
            ...     source=source,
            ...     )
            Delay1.ar()

        Returns unit generator graph.
        """
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
        """
        Constructs a control-rate one-sample delay line.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.Delay1.kr(
            ...     source=source,
            ...     )
            Delay1.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of Delay1.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> delay_1 = ugentools.Delay1.ar(
            ...     source=source,
            ...     )
            >>> delay_1.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
