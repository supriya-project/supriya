import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class DiskOut(UGen):
    """
    Records to a soundfile to disk.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
        >>> disk_out = supriya.ugens.DiskOut.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        >>> disk_out
        DiskOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Disk I/O UGens"

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("source", None)]
    )

    _unexpanded_input_names = ("source",)

    _valid_calculation_rates = (CalculationRate.AUDIO,)
