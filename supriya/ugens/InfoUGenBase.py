from supriya.ugens.UGen import UGen


class InfoUGenBase(UGen):
    """
    Abstract base class for scalar-rate information ugens.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        """
        Constructs a scalar-rate information ugen.

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            **kwargs
            )
        return ugen
