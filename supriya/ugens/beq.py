import collections

from supriya import CalculationRate
from supriya.ugens.filters import Filter


class BEQSuite(Filter):
    """
    Abstract base class of all BEQSuite UGens.
    """


class BAllPass(BEQSuite):
    """
    An all-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> ball_pass = supriya.ugens.BAllPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> ball_pass
        BAllPass.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_q", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BBandPass(BEQSuite):
    """
    A band-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bband_pass = supriya.ugens.BBandPass.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ... )
        >>> bband_pass
        BBandPass.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("bandwidth", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BBandStop(BEQSuite):
    """
    A band-stop filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bband_stop = supriya.ugens.BBandStop.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ... )
        >>> bband_stop
        BBandStop.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("bandwidth", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BHiCut(BEQSuite):
    """
    A high-cut filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bhi_cut = supriya.ugens.BHiCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ... )
        >>> bhi_cut
        BHiCut.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("order", 2), ("max_order", 5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BHiPass(BEQSuite):
    """
    A high-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bhi_pass = supriya.ugens.BHiPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> bhi_pass
        BHiPass.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_q", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BHiShelf(BEQSuite):
    """
    A high-shelf filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
        ...     gain=0,
        ...     frequency=1200,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ... )
        >>> bhi_shelf
        BHiShelf.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_s", 1), ("gain", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BLowCut(BEQSuite):
    """
    A low-cut filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> blow_cut = supriya.ugens.BLowCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ... )
        >>> blow_cut
        BLowCut.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("order", 2), ("max_order", 5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BLowPass(BEQSuite):
    """
    A low-pass filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> blow_pass = supriya.ugens.BLowPass.ar(
        ...     frequency=1200,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> blow_pass
        BLowPass.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_q", 1)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BLowShelf(BEQSuite):
    """
    A low-shelf filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> blow_shelf = supriya.ugens.BLowShelf.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ... )
        >>> blow_shelf
        BLowShelf.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_s", 1), ("gain", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class BPeakEQ(BEQSuite):
    """
    A parametric equalizer.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bpeak_eq = supriya.ugens.BPeakEQ.ar(
        ...     frequency=1200,
        ...     gain=0,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ... )
        >>> bpeak_eq
        BPeakEQ.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("frequency", 1200), ("reciprocal_of_q", 1), ("gain", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)
