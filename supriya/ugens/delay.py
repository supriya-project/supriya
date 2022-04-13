import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen, UGen


class AllpassC(PureUGen):
    """
    A cubic-interpolating allpass delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_c = supriya.ugens.AllpassC.ar(source=source)
        >>> allpass_c
        AllpassC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class AllpassL(PureUGen):
    """
    A linear interpolating allpass delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_l = supriya.ugens.AllpassL.ar(source=source)
        >>> allpass_l
        AllpassL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class AllpassN(PureUGen):
    """
    A non-interpolating allpass delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_n = supriya.ugens.AllpassN.ar(source=source)
        >>> allpass_n
        AllpassN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BufAllpassC(PureUGen):
    """
    A buffer-based cubic-interpolating allpass delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufAllpassC.ar()

    """

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


class BufAllpassL(PureUGen):
    """
    A buffer-based linear-interpolating allpass delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufAllpassL.ar()

    """

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


class BufAllpassN(PureUGen):
    """
    A buffer-based non-interpolating allpass delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufAllpassN.ar()

    """

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


class BufCombC(PureUGen):
    """
    A buffer-based cubic-interpolating comb delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufCombC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.AUDIO)


class BufCombL(PureUGen):
    """
    A buffer-based linear-interpolating comb delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufCombL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.AUDIO)


class BufCombN(PureUGen):
    """
    A buffer-based non-interpolating comb delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufCombN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.AUDIO)


class BufDelayC(PureUGen):
    """
    A buffer-based cubic-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufDelayC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BufDelayL(PureUGen):
    """
    A buffer-based linear-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufDelayL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class BufDelayN(PureUGen):
    """
    A buffer-based non-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        BufDelayN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class CombC(PureUGen):
    """
    A cubic-interpolating comb delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombC.ar(source=source)
        CombC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class CombL(PureUGen):
    """
    A linear interpolating comb delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombL.ar(source=source)
        CombL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class CombN(PureUGen):
    """
    A non-interpolating comb delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombN.ar(source=source)
        CombN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
            ("decay_time", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DelTapRd(UGen):
    """
    A delay tap reader unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(0)
        >>> tapin = supriya.ugens.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )

    ::

        >>> tapin
        DelTapWr.ar()

    ::

        >>> tapout = supriya.ugens.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ... )

    ::

        >>> tapout
        DelTapRd.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("phase", None),
            ("delay_time", 0.0),
            ("interpolation", 1.0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DelTapWr(UGen):
    """
    A delay tap writer unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(0)
        >>> tapin = supriya.ugens.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )

    ::

        >>> tapin
        DelTapWr.ar()

    ::

        >>> tapout = supriya.ugens.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ... )

    ::

        >>> tapout
        DelTapRd.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("source", None)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DelayC(PureUGen):
    """
    A cubic-interpolating delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayC.ar(source=source)
        DelayC.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("maximum_delay_time", 0.2), ("delay_time", 0.2)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DelayL(PureUGen):
    """
    A linear-interpolating delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayL.ar(source=source)
        DelayL.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("maximum_delay_time", 0.2), ("delay_time", 0.2)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DelayN(PureUGen):
    """
    A non-interpolating delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayN.ar(source=source)
        DelayN.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("maximum_delay_time", 0.2), ("delay_time", 0.2)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Delay1(PureUGen):
    """
    A one-sample delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay1.ar(source=source)
        Delay1.ar()

    """

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Delay2(PureUGen):
    """
    A two-sample delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay2.ar(source=source)
        Delay2.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("maximum_delay_time", 0.2), ("delay_time", 0.2)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
