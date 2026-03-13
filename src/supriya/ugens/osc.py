from typing import Any

from ..enums import CalculationRate, DoneAction
from .core import UGen, param, ugen


@ugen(ar=True, kr=True, is_pure=True)
class COsc(UGen):
    """
    A chorusing wavetable oscillator.

    ::

        >>> cosc = supriya.ugens.COsc.ar(
        ...     beats=0.5,
        ...     buffer_id=23,
        ...     frequency=440,
        ... )
        >>> cosc
        <COsc.ar()[0]>
    """

    buffer_id = param()
    frequency = param(440.0)
    beats = param(0.5)


@ugen(ar=True, kr=True, is_pure=True)
class DegreeToKey(UGen):
    """
    A signal-to-modal-pitch converter.`

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> degree_to_key = supriya.ugens.DegreeToKey.ar(
        ...     buffer_id=23,
        ...     octave=12,
        ...     source=source,
        ... )
        >>> degree_to_key
        <DegreeToKey.ar()[0]>
    """

    buffer_id = param()
    source = param()
    octave = param(12)


@ugen(ar=True, kr=True, is_pure=True)
class Impulse(UGen):
    """
    A non-band-limited single-sample impulse generator unit generator.

    ::

        >>> supriya.ugens.Impulse.ar()
        <Impulse.ar()[0]>
    """

    frequency = param(440.0)
    phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class Index(UGen):
    """
    A clipping buffer indexer.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> index = supriya.ugens.Index.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> index
        <Index.ar()[0]>
    """

    buffer_id = param()
    source = param()


@ugen(ar=True, kr=True, is_pure=True)
class LFCub(UGen):
    """
    A sine-like oscillator unit generator.

    ::

        >>> supriya.ugens.LFCub.ar()
        <LFCub.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class LFGauss(UGen):
    """
    A non-band-limited gaussian function oscillator.

    ::

        >>> supriya.ugens.LFGauss.ar()
        <LFGauss.ar()[0]>
    """

    duration = param(1)
    width = param(0.1)
    initial_phase = param(0)
    loop = param(1)
    done_action = param(0)

    def _postprocess_kwargs(
        self,
        *,
        calculation_rate: CalculationRate,
        **kwargs,
    ) -> tuple[CalculationRate, dict[str, Any]]:
        return calculation_rate, {
            **kwargs,
            "done_action": DoneAction.from_expr(int(kwargs["done_action"])),
        }


@ugen(ar=True, kr=True, is_pure=True)
class LFPar(UGen):
    """
    A parabolic oscillator unit generator.

    ::

        >>> supriya.ugens.LFPar.ar()
        <LFPar.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class LFPulse(UGen):
    """
    A non-band-limited pulse oscillator.

    ::

        >>> supriya.ugens.LFPulse.ar()
        <LFPulse.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)
    width = param(0.5)


@ugen(ar=True, kr=True, is_pure=True)
class LFSaw(UGen):
    """
    A non-band-limited sawtooth oscillator unit generator.

    ::

        >>> supriya.ugens.LFSaw.ar()
        <LFSaw.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class LFTri(UGen):
    """
    A non-band-limited triangle oscillator unit generator.

    ::

        >>> supriya.ugens.LFTri.ar()
        <LFTri.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class Osc(UGen):
    """
    An interpolating wavetable oscillator.
    """

    buffer_id = param()
    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class OscN(UGen):
    """
    A non-interpolating wavetable oscillator.
    """

    buffer_id = param()
    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class Select(UGen):
    """
    A signal selector.

    ::

        >>> sources = supriya.ugens.In.ar(bus=0, channel_count=8)
        >>> selector = supriya.ugens.Phasor.kr() * 8
        >>> select = supriya.ugens.Select.ar(
        ...     sources=sources,
        ...     selector=selector,
        ... )
        >>> select
        <Select.ar()[0]>
    """

    selector = param()
    sources = param(unexpanded=True)


@ugen(ar=True, kr=True, is_pure=True)
class SinOsc(UGen):
    """
    A sinusoid oscillator unit generator.

    ::

        >>> supriya.ugens.SinOsc.ar()
        <SinOsc.ar()[0]>

    ::

        >>> print(_)
        synthdef:
            name: ...
            ugens:
            -   SinOsc.ar:
                    frequency: 440.0
                    phase: 0.0
    """

    frequency = param(440.0)
    phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class SyncSaw(UGen):
    """
    A sawtooth wave that is hard synched to a fundamental pitch.

    ::

        >>> sync_saw = supriya.ugens.SyncSaw.ar(
        ...     saw_frequency=440,
        ...     sync_frequency=440,
        ... )
        >>> sync_saw
        <SyncSaw.ar()[0]>
    """

    sync_frequency = param(440.0)
    saw_frequency = param(440.0)


@ugen(ar=True, kr=True, is_pure=True)
class VOsc(UGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc = supriya.ugens.VOsc.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(minimum=0, maximum=7),
        ...     frequency=440,
        ...     phase=0,
        ... )
        >>> vosc
        <VOsc.ar()[0]>
    """

    buffer_id = param()
    frequency = param(440.0)
    phase = param(0.0)


@ugen(ar=True, kr=True, is_pure=True)
class VOsc3(UGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc_3 = supriya.ugens.VOsc3.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(minimum=0, maximum=7),
        ...     freq_1=110,
        ...     freq_2=220,
        ...     freq_3=440,
        ... )
        >>> vosc_3
        <VOsc3.ar()[0]>
    """

    buffer_id = param()
    freq_1 = param(110.0)
    freq_2 = param(220.0)
    freq_3 = param(440.0)


@ugen(ar=True, kr=True, is_pure=True)
class VarSaw(UGen):
    """
    A sawtooth-triangle oscillator with variable duty.

    ::

        >>> supriya.ugens.VarSaw.ar()
        <VarSaw.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)
    width = param(0.5)


@ugen(ar=True, kr=True, is_pure=True)
class Vibrato(UGen):
    """
    Vibrato is a slow frequency modulation.

    ::

        >>> vibrato = supriya.ugens.Vibrato.ar(
        ...     delay=0,
        ...     depth=0.02,
        ...     depth_variation=0.1,
        ...     frequency=440,
        ...     initial_phase=0,
        ...     onset=0,
        ...     rate=6,
        ...     rate_variation=0.04,
        ... )
        >>> vibrato
        <Vibrato.ar()[0]>
    """

    frequency = param(440)
    rate = param(6)
    depth = param(0.02)
    delay = param(0)
    onset = param(0)
    rate_variation = param(0.04)
    depth_variation = param(0.1)
    initial_phase = param(0)


@ugen(ar=True, kr=True, is_pure=True)
class WrapIndex(UGen):
    """
    A wrapping buffer indexer.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> wrap_index = supriya.ugens.WrapIndex.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> wrap_index
        <WrapIndex.ar()[0]>
    """

    buffer_id = param()
    source = param()
