import collections
from uqbar.enums import IntEnumeration


__all__ = [
    'AddAction',
    'CalculationRate',
    ]


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

    @staticmethod
    def from_collection(collection):
        """
        Gets calculation-rate from a collection.

        ::

            >>> import supriya.synthdefs
            >>> import supriya.ugens

        ::

            >>> collection = []
            >>> collection.append(supriya.ugens.DC.ar(0))
            >>> collection.append(supriya.ugens.DC.kr(1))
            >>> collection.append(2.0)
            >>> supriya.CalculationRate.from_collection(collection)
            CalculationRate.AUDIO

        ::
            >>> collection = []
            >>> collection.append(supriya.ugens.DC.kr(1))
            >>> collection.append(2.0)
            >>> supriya.CalculationRate.from_collection(collection)
            CalculationRate.CONTROL

        Return calculation-rate.
        """
        rates = [
            CalculationRate.from_input(item) for item in collection
            ]
        maximum_rate = max(rates)
        return maximum_rate

    @staticmethod
    def from_input(input_):
        import supriya.synthdefs
        import supriya.ugens
        if isinstance(input_, (int, float)):
            return CalculationRate.SCALAR
        elif isinstance(input_, (
            supriya.synthdefs.OutputProxy,
            supriya.ugens.UGen,
            )):
            return input_.calculation_rate
        elif isinstance(input_, supriya.synthdefs.Parameter):
            name = input_.parameter_rate.name
            if name == 'TRIGGER':
                return CalculationRate.CONTROL
            return CalculationRate.from_expr(name)
        elif isinstance(input_, collections.Sequence):
            return CalculationRate.from_collection(input_)
        elif hasattr(input_, 'calculation_rate'):
            return Calculation.from_expr(input_.calculation_rate)
        raise ValueError(input_)

    @staticmethod
    def from_ugen_method_mixin(expr):
        if isinstance(expr, collections.Sequence):
            return CalculationRate.from_collection(expr)
        return CalculationRate.from_input(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def token(self):
        if self == CalculationRate.SCALAR:
            return 'ir'
        elif self == CalculationRate.CONTROL:
            return 'kr'
        elif self == CalculationRate.AUDIO:
            return 'ar'
        return '--'
