from supriya.ugens.UGen import UGen


class PinkNoise(UGen):
    """
    A pink noise unit generator.

    ::

        >>> supriya.ugens.PinkNoise.ar()
        PinkNoise.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        ):
        """
        Constructs an audio-rate pink noise unit generator.

        ::

            >>> supriya.ugens.PinkNoise.ar()
            PinkNoise.ar()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        ):
        """
        Constructs a control-rate pink noise unit generator.

        ::

            >>> supriya.ugens.PinkNoise.kr()
            PinkNoise.kr()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            )
        return ugen
