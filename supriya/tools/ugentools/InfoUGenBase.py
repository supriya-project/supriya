from supriya.tools.ugentools.UGen import UGen


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
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            **kwargs
            )
        return ugen
