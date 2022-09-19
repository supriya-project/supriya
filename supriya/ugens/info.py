from .bases import UGen, param, ugen


@ugen(ir=True)
class BlockSize(UGen):
    """
    A block size info unit generator.

    ::

        >>> supriya.ugens.BlockSize.ir()
        BlockSize.ir()

    """


@ugen(kr=True, ir=True)
class BufChannels(UGen):
    """
    A buffer channel count info unit generator.

    ::

        >>> supriya.ugens.BufChannels.kr(buffer_id=0)
        BufChannels.kr()

    """

    buffer_id = param(None)


@ugen(kr=True, ir=True)
class BufDur(UGen):
    """
    A buffer duration info unit generator.

    ::

        >>> supriya.ugens.BufDur.kr(buffer_id=0)
        BufDur.kr()

    """

    buffer_id = param(None)


@ugen(kr=True, ir=True)
class BufFrames(UGen):
    """
    A buffer frame count info unit generator.

    ::

        >>> supriya.ugens.BufFrames.kr(buffer_id=0)
        BufFrames.kr()

    """

    buffer_id = param(None)


@ugen(kr=True, ir=True)
class BufRateScale(UGen):
    """
    A buffer sample-rate scale info unit generator.

    ::

        >>> supriya.ugens.BufRateScale.kr(buffer_id=0)
        BufRateScale.kr()

    """

    buffer_id = param(None)


@ugen(kr=True, ir=True)
class BufSampleRate(UGen):
    """
    A buffer sample-rate info unit generator.

    ::

        >>> supriya.ugens.BufSampleRate.kr(buffer_id=0)
        BufSampleRate.kr()

    """

    buffer_id = param(None)


@ugen(kr=True, ir=True)
class BufSamples(UGen):
    """
    A buffer sample count info unit generator.

    ::

        >>> supriya.ugens.BufSamples.kr(buffer_id=0)
        BufSamples.kr()

    """

    buffer_id = param(None)


@ugen(ir=True)
class ControlDur(UGen):
    """
    A control duration info unit generator.

    ::

        >>> supriya.ugens.ControlDur.ir()
        ControlDur.ir()

    """


@ugen(ir=True)
class ControlRate(UGen):
    """
    A control rate info unit generator.

    ::

        >>> supriya.ugens.ControlRate.ir()
        ControlRate.ir()

    """


@ugen(ir=True)
class NodeID(UGen):
    """
    A node ID info unit generator.

    ::

        >>> supriya.ugens.NodeID.ir()
        NodeID.ir()

    """


@ugen(ir=True)
class NumAudioBuses(UGen):
    """
    A number of audio buses info unit generator.

    ::

        >>> supriya.ugens.NumAudioBuses.ir()
        NumAudioBuses.ir()

    """


@ugen(ir=True)
class NumBuffers(UGen):
    """
    A number of buffers info unit generator.

    ::

        >>> supriya.ugens.NumBuffers.ir()
        NumBuffers.ir()

    """


@ugen(ir=True)
class NumControlBuses(UGen):
    """
    A number of control buses info unit generator.

    ::

        >>> supriya.ugens.NumControlBuses.ir()
        NumControlBuses.ir()

    """


@ugen(ir=True)
class NumInputBuses(UGen):
    """
    A number of input buses info unit generator.

    ::

        >>> supriya.ugens.NumInputBuses.ir()
        NumInputBuses.ir()

    """


@ugen(ir=True)
class NumOutputBuses(UGen):
    """
    A number of output buses info unit generator.

    ::

        >>> supriya.ugens.NumOutputBuses.ir()
        NumOutputBuses.ir()

    """


@ugen(kr=True, ir=True)
class NumRunningSynths(UGen):
    """
    A number of running synths info unit generator.

    ::

        >>> supriya.ugens.NumRunningSynths.ir()
        NumRunningSynths.ir()

    """


@ugen(ir=True)
class RadiansPerSample(UGen):
    """
    A radians-per-sample info unit generator.

    ::

        >>> supriya.ugens.RadiansPerSample.ir()
        RadiansPerSample.ir()

    """


@ugen(ir=True)
class SampleDur(UGen):
    """
    A sample duration info unit generator.

    ::

        >>> supriya.ugens.SampleDur.ir()
        SampleDur.ir()

    """


@ugen(ir=True)
class SampleRate(UGen):
    """
    A sample-rate info unit generator.

    ::

        >>> supriya.ugens.SampleRate.ir()
        SampleRate.ir()

    """


@ugen(ir=True)
class SubsampleOffset(UGen):
    """
    A subsample-offset info unit generator.

    ::

        >>> supriya.ugens.SubsampleOffset.ir()
        SubsampleOffset.ir()

    """
