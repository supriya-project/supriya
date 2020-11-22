import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen
from supriya.typing import UGenInputMap


class BlockSize(UGen):
    """
    A block size info unit generator.

    ::

        >>> supriya.ugens.BlockSize.ir()
        BlockSize.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class BufChannels(UGen):
    """
    A buffer channel count info unit generator.

    ::

        >>> supriya.ugens.BufChannels.kr(buffer_id=0)
        BufChannels.kr()

    """

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class BufDur(UGen):
    """
    A buffer duration info unit generator.

    ::

        >>> supriya.ugens.BufDur.kr(buffer_id=0)
        BufDur.kr()

    """

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class BufFrames(UGen):
    """
    A buffer frame count info unit generator.

    ::

        >>> supriya.ugens.BufFrames.kr(buffer_id=0)
        BufFrames.kr()

    """

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class BufRateScale(UGen):
    """
    A buffer sample-rate scale info unit generator.

    ::

        >>> supriya.ugens.BufRateScale.kr(buffer_id=0)
        BufRateScale.kr()

    """

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class BufSampleRate(UGen):
    """
    A buffer sample-rate info unit generator.

    ::

        >>> supriya.ugens.BufSampleRate.kr(buffer_id=0)
        BufSampleRate.kr()

    """

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class BufSamples(UGen):
    """
    A buffer sample count info unit generator.

    ::

        >>> supriya.ugens.BufSamples.kr(buffer_id=0)
        BufSamples.kr()

    """

    _ordered_input_names = collections.OrderedDict([("buffer_id", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class ControlDur(UGen):
    """
    A control duration info unit generator.

    ::

        >>> supriya.ugens.ControlDur.ir()
        ControlDur.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class ControlRate(UGen):
    """
    A control rate info unit generator.

    ::

        >>> supriya.ugens.ControlRate.ir()
        ControlRate.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class NodeID(UGen):
    """
    A node ID info unit generator.

    ::

        >>> supriya.ugens.NodeID.ir()
        NodeID.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class NumAudioBuses(UGen):
    """
    A number of audio buses info unit generator.

    ::

        >>> supriya.ugens.NumAudioBuses.ir()
        NumAudioBuses.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class NumBuffers(UGen):
    """
    A number of buffers info unit generator.

    ::

        >>> supriya.ugens.NumBuffers.ir()
        NumBuffers.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class NumControlBuses(UGen):
    """
    A number of control buses info unit generator.

    ::

        >>> supriya.ugens.NumControlBuses.ir()
        NumControlBuses.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class NumInputBuses(UGen):
    """
    A number of input buses info unit generator.

    ::

        >>> supriya.ugens.NumInputBuses.ir()
        NumInputBuses.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class NumOutputBuses(UGen):
    """
    A number of output buses info unit generator.

    ::

        >>> supriya.ugens.NumOutputBuses.ir()
        NumOutputBuses.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class NumRunningSynths(UGen):
    """
    A number of running synths info unit generator.

    ::

        >>> supriya.ugens.NumRunningSynths.ir()
        NumRunningSynths.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.CONTROL, CalculationRate.SCALAR)


class RadiansPerSample(UGen):
    """
    A radians-per-sample info unit generator.

    ::

        >>> supriya.ugens.RadiansPerSample.ir()
        RadiansPerSample.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class SampleDur(UGen):
    """
    A sample duration info unit generator.

    ::

        >>> supriya.ugens.SampleDur.ir()
        SampleDur.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class SampleRate(UGen):
    """
    A sample-rate info unit generator.

    ::

        >>> supriya.ugens.SampleRate.ir()
        SampleRate.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)


class SubsampleOffset(UGen):
    """
    A subsample-offset info unit generator.

    ::

        >>> supriya.ugens.SubsampleOffset.ir()
        SubsampleOffset.ir()

    """

    _ordered_input_names: UGenInputMap = collections.OrderedDict([])
    _valid_calculation_rates = (CalculationRate.SCALAR,)
