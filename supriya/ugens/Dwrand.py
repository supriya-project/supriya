import collections
from supriya import CalculationRate
from supriya.ugens.DUGen import DUGen


class Dwrand(DUGen):
    """
    A demand-rate weighted random sequence generator.

    ::

        >>> sequence = [0, 1, 2, 7]
        >>> weights = [0.4, 0.4, 0.1, 0.1]
        >>> dwrand = supriya.ugens.Dwrand.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     weights=weights,
        ...     )
        >>> dwrand
        Dwrand()

    """

    ### CLASS VARIABLES ###

    # TODO: We should not include length in the generated methods

    _ordered_input_names = collections.OrderedDict(
        [('repeats', 1), ('length', None), ('weights', None), ('sequence', None)]
    )

    _unexpanded_input_names = ('weights', 'sequence')

    _valid_calculation_rates = (CalculationRate.DEMAND,)

    ### INITIALIZER ###

    def __init__(self, repeats=1, sequence=None, weights=None, **kwargs):
        if not isinstance(sequence, collections.Sequence):
            sequence = [sequence]
        sequence = tuple(float(_) for _ in sequence)
        if not isinstance(weights, collections.Sequence):
            weights = [weights]
        weights = tuple(float(_) for _ in weights)
        weights = weights[: len(sequence)]
        weights += (0.0,) * (len(sequence) - len(weights))
        DUGen.__init__(
            self,
            repeats=repeats,
            length=len(sequence),
            sequence=sequence,
            weights=weights,
        )
