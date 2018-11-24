import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class LinExp(PureUGen):
    """
    A linear-to-exponential range mapper.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> lin_exp = supriya.ugens.LinExp.ar(
        ...     input_maximum=1.0,
        ...     input_minimum=-1.0,
        ...     output_maximum=22050,
        ...     output_minimum=20,
        ...     source=source,
        ...     )
        >>> lin_exp
        LinExp.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Line Utility UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("input_minimum", 0),
            ("input_maximum", 1),
            ("output_minimum", 1),
            ("output_maximum", 2),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
