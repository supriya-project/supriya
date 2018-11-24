import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class RecordBuf(UGen):
    """
    Records or overdubs into a buffer.

    ::

        >>> buffer_id = 23
        >>> source = supriya.ugens.SoundIn.ar(bus=(0, 1))
        >>> record_buf = supriya.ugens.RecordBuf.ar(
        ...     buffer_id=buffer_id,
        ...     done_action=0,
        ...     loop=1,
        ...     offset=0,
        ...     preexisting_level=0,
        ...     record_level=1,
        ...     run=1,
        ...     source=source,
        ...     trigger=1,
        ...     )
        >>> record_buf
        RecordBuf.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Buffer UGens"

    _has_done_flag = True

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("offset", 0),
            ("record_level", 1),
            ("preexisting_level", 0),
            ("run", 1),
            ("loop", 1),
            ("trigger", 1),
            ("done_action", 0),
            ("source", None),
        ]
    )

    _unexpanded_input_names = ("source",)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
