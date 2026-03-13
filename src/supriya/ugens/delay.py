from .core import UGen, param, ugen


@ugen(ar=True, kr=True, is_pure=True)
class AllpassC(UGen):
    """
    A cubic-interpolating allpass delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_c = supriya.ugens.AllpassC.ar(source=source)
        >>> allpass_c
        <AllpassC.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class AllpassL(UGen):
    """
    A linear interpolating allpass delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_l = supriya.ugens.AllpassL.ar(source=source)
        >>> allpass_l
        <AllpassL.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class AllpassN(UGen):
    """
    A non-interpolating allpass delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> allpass_n = supriya.ugens.AllpassN.ar(source=source)
        >>> allpass_n
        <AllpassN.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class BufAllpassC(UGen):
    """
    A buffer-based cubic-interpolating allpass delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufAllpassC.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class BufAllpassL(UGen):
    """
    A buffer-based linear-interpolating allpass delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufAllpassL.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class BufAllpassN(UGen):
    """
    A buffer-based non-interpolating allpass delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufAllpassN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufAllpassN.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class BufCombC(UGen):
    """
    A buffer-based cubic-interpolating comb delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufCombC.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class BufCombL(UGen):
    """
    A buffer-based linear-interpolating comb delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufCombL.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class BufCombN(UGen):
    """
    A buffer-based non-interpolating comb delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufCombN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufCombN.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class BufDelayC(UGen):
    """
    A buffer-based cubic-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayC.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufDelayC.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)


@ugen(ar=True, kr=True, is_pure=True)
class BufDelayL(UGen):
    """
    A buffer-based linear-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufDelayL.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)


@ugen(ar=True, kr=True, is_pure=True)
class BufDelayN(UGen):
    """
    A buffer-based non-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayN.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )
        <BufDelayN.ar()[0]>
    """

    buffer_id = param()
    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)


@ugen(ar=True, kr=True, is_pure=True)
class CombC(UGen):
    """
    A cubic-interpolating comb delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombC.ar(source=source)
        <CombC.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class CombL(UGen):
    """
    A linear interpolating comb delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombL.ar(source=source)
        <CombL.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class CombN(UGen):
    """
    A non-interpolating comb delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.CombN.ar(source=source)
        <CombN.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)
    decay_time = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class DelTapRd(UGen):
    """
    A delay tap reader unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> tapin = supriya.ugens.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )

    ::

        >>> tapin
        <DelTapWr.ar()[0]>

    ::

        >>> tapout = supriya.ugens.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ... )

    ::

        >>> tapout
        <DelTapRd.ar()[0]>
    """

    buffer_id = param()
    phase = param()
    delay_time = param(0.0)
    interpolation = param(1.0)


@ugen(ar=True, kr=True, is_pure=True)
class DelTapWr(UGen):
    """
    A delay tap writer unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> tapin = supriya.ugens.DelTapWr.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ... )

    ::

        >>> tapin
        <DelTapWr.ar()[0]>

    ::

        >>> tapout = supriya.ugens.DelTapRd.ar(
        ...     buffer_id=buffer_id,
        ...     phase=tapin,
        ...     delay_time=0.1,
        ...     interpolation=True,
        ... )

    ::

        >>> tapout
        <DelTapRd.ar()[0]>
    """

    buffer_id = param()
    source = param()


@ugen(ar=True, kr=True, is_pure=True)
class DelayC(UGen):
    """
    A cubic-interpolating delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayC.ar(source=source)
        <DelayC.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)


@ugen(ar=True, kr=True, is_pure=True)
class DelayL(UGen):
    """
    A linear-interpolating delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayL.ar(source=source)
        <DelayL.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)


@ugen(ar=True, kr=True, is_pure=True)
class DelayN(UGen):
    """
    A non-interpolating delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.DelayN.ar(source=source)
        <DelayN.ar()[0]>
    """

    source = param()
    maximum_delay_time = param(0.2)
    delay_time = param(0.2)


@ugen(ar=True, kr=True, is_pure=True)
class Delay1(UGen):
    """
    A one-sample delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay1.ar(source=source)
        <Delay1.ar()[0]>
    """

    source = param()


@ugen(ar=True, kr=True, is_pure=True)
class Delay2(UGen):
    """
    A two-sample delay line unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.Delay2.ar(source=source)
        <Delay2.ar()[0]>
    """

    source = param()
