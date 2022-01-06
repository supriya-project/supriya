import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class CheckBadValues(UGen):
    """
    Tests for infinity, not-a-number, and denormals.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> ugen_id = 23
        >>> post_mode = 0
        >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
        ...     source=source,
        ...     ugen_id=ugen_id,
        ...     post_mode=post_mode,
        ... )
        >>> check_bad_values
        CheckBadValues.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("ugen_id", 0.0), ("post_mode", 2.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, ugen_id=0, post_mode=2, source=None):
        assert int(post_mode) in (0, 1, 2)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
        )


class Sanitize(UGen):
    """
    Remove infinity, NaN, and denormals.
    """

    _ordered_input_names = collections.OrderedDict([("source", None), ("replace", 0.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
