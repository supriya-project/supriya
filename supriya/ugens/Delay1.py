from supriya.ugens.PureUGen import PureUGen


class Delay1(PureUGen):
    """
    A one-sample delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay1.ar(source=source)
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

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> supriya.ugens.Delay1.ar(
            ...     source=source,
            ...     )
            Delay1.ar()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
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

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> supriya.ugens.Delay1.kr(
            ...     source=source,
            ...     )
            Delay1.ar()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
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

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> delay_1 = supriya.ugens.Delay1.ar(
            ...     source=source,
            ...     )
            >>> delay_1.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
