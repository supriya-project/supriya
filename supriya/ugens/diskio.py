import collections

from supriya import CalculationRate
from supriya.synthdefs import MultiOutUGen, UGen


class DiskIn(MultiOutUGen):
    """
    Streams in audio from a file.

    ::

        >>> buffer_id = 23
        >>> disk_in = supriya.ugens.DiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ... )
        >>> disk_in
        UGenArray({2})

    """

    _default_channel_count = 1
    _has_done_flag = True
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict([("buffer_id", None), ("loop", 0.0)])
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class DiskOut(UGen):
    """
    Records to a soundfile to disk.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
        >>> disk_out = supriya.ugens.DiskOut.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        >>> disk_out
        DiskOut.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("source", None)]
    )
    _unexpanded_input_names = ("source",)
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class VDiskIn(MultiOutUGen):
    """
    Streams in audio from a file, with variable rate.

    ::

        >>> buffer_id = 23
        >>> vdisk_in = supriya.ugens.VDiskIn.ar(
        ...     buffer_id=buffer_id,
        ...     channel_count=2,
        ...     loop=0,
        ...     rate=1,
        ...     send_id=0,
        ... )
        >>> vdisk_in
        UGenArray({2})

    """

    _default_channel_count = 1
    _has_done_flag = True
    _has_settable_channel_count = True
    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("rate", 1), ("loop", 0), ("send_id", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)
