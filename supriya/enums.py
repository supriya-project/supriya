import collections
from uqbar.enums import IntEnumeration


__all__ = ["AddAction", "CalculationRate"]


class AddAction(IntEnumeration):
    """
    An enumeration of scsynth node add actions.
    """

    ### CLASS VARIABLES ###

    ADD_TO_HEAD = 0
    ADD_TO_TAIL = 1
    ADD_BEFORE = 2
    ADD_AFTER = 3
    REPLACE = 4


class CalculationRate(IntEnumeration):
    """
    An enumeration of scsynth calculation-rates.

    ::

        >>> import supriya.synthdefs
        >>> supriya.CalculationRate.AUDIO
        CalculationRate.AUDIO

    ::

        >>> supriya.CalculationRate.from_expr('demand')
        CalculationRate.DEMAND

    """

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 1
    DEMAND = 3
    SCALAR = 0

    ### PUBLIC METHODS ###

    @classmethod
    def from_expr(cls, expr):
        """
        Gets calculation-rate.

        ::

            >>> import supriya.synthdefs
            >>> import supriya.ugens

        ::

            >>> supriya.CalculationRate.from_expr(1)
            CalculationRate.SCALAR

        ::

            >>> supriya.CalculationRate.from_expr('demand')
            CalculationRate.DEMAND

        ::

            >>> collection = []
            >>> collection.append(supriya.ugens.DC.ar(0))
            >>> collection.append(supriya.ugens.DC.kr(1))
            >>> collection.append(2.0)
            >>> supriya.CalculationRate.from_expr(collection)
            CalculationRate.AUDIO

        ::
            >>> collection = []
            >>> collection.append(supriya.ugens.DC.kr(1))
            >>> collection.append(2.0)
            >>> supriya.CalculationRate.from_expr(collection)
            CalculationRate.CONTROL

        Return calculation-rate.
        """
        import supriya.synthdefs
        import supriya.ugens

        if isinstance(expr, (int, float)) and not isinstance(expr, cls):
            return CalculationRate.SCALAR
        elif isinstance(expr, (supriya.synthdefs.OutputProxy, supriya.ugens.UGen)):
            return expr.calculation_rate
        elif isinstance(expr, supriya.synthdefs.Parameter):
            name = expr.parameter_rate.name
            if name == "TRIGGER":
                return CalculationRate.CONTROL
            return CalculationRate.from_expr(name)
        elif isinstance(expr, str):
            return super().from_expr(expr)
        elif isinstance(expr, collections.Sequence):
            return max(CalculationRate.from_expr(item) for item in expr)
        elif hasattr(expr, "calculation_rate"):
            return cls.from_expr(expr.calculation_rate)
        return super().from_expr(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def token(self):
        if self == CalculationRate.SCALAR:
            return "ir"
        elif self == CalculationRate.CONTROL:
            return "kr"
        elif self == CalculationRate.AUDIO:
            return "ar"
        return "new"
