from .bases import UGen, param, ugen


@ugen(ar=True)
class Convolution(UGen):
    """
    A real-time convolver.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution = supriya.ugens.Convolution.ar(
        ...     framesize=512,
        ...     kernel=kernel,
        ...     source=source,
        ... )
        >>> convolution
        Convolution.ar()

    """

    source = param(None)
    kernel = param(None)
    framesize = param(512)


@ugen(ar=True)
class Convolution2(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger
    signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_2 = supriya.ugens.Convolution2.ar(
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_2
        Convolution2.ar()

    """

    source = param(None)
    kernel = param(None)
    trigger = param(0.0)
    framesize = param(2048)


@ugen(ar=True)
class Convolution2L(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_2_l = supriya.ugens.Convolution2L.ar(
        ...     crossfade=1,
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_2_l
        Convolution2L.ar()

    """

    source = param(None)
    kernel = param(None)
    trigger = param(0.0)
    framesize = param(2048)
    crossfade = param(1.0)


@ugen(ar=True)
class Convolution3(UGen):
    """
    Strict convolution with fixed kernel which can be updated using a trigger signal.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> kernel = supriya.ugens.Mix.new(
        ...     supriya.ugens.LFSaw.ar(frequency=[300, 500, 800, 1000])
        ...     * supriya.ugens.MouseX.kr(minimum=1, maximum=2),
        ... )
        >>> convolution_3 = supriya.ugens.Convolution3.ar(
        ...     framesize=2048,
        ...     kernel=kernel,
        ...     source=source,
        ...     trigger=0,
        ... )
        >>> convolution_3
        Convolution3.ar()

    """

    source = param(None)
    kernel = param(None)
    trigger = param(0.0)
    framesize = param(2048)
