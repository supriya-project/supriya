import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen


class BufAllpassN(PureUGen):
    """
    A buffer-based non-interpolating allpass delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufAllpassN.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Delay UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
