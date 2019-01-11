from supriya.synthdefs import Envelope, Parameter, SynthDefBuilder
from supriya.ugens import LPF, Balance2, LFNoise2, Out, Pulse, Splay


"""
(
SynthDef(\pad, {
    var snd, freq;
    freq = \freq.kr(440);
    // Four pulse waves (two one octave down) with randomly modulated pitches and pulse widths
    snd = Pulse.ar(
        freq * ({ LFNoise2.kr(3).range(-0.05, 0.05).midiratio }.dup(4)) * [1, 1/2, 1/2, 1],
        { LFNoise2.kr(3).range(0.3, 0.7) }.dup(4)
    );
    // Spread across stereo field
    snd = Splay.ar(snd);
    // Sharp hi cut made by cascading three lowpass filters
    3.do { snd = LPF.ar(snd, \ffreq.kr(1500)); };
    snd = snd * Env.asr(3, 1, 3, -4).ar(Done.freeSelf, \gate.kr(1));
    Out.ar(\out.kr(0), Balance2.ar(snd[0], snd[1], \pan.kr(0), \amp.kr(0.1)));
}).add;
"""


def _build_synthdef():
    builder = SynthDefBuilder(
        amplitude=0.1,
        filter_frequency=1500,
        frequency=440,
        gate=1,
        out=Parameter(parameter_rate="scalar", value=0),
        pan=0,
    )
    with builder:
        frequencies, widths = [], []
        for multiplier in [1, 0.5, 0.5, 1]:
            frequencies.append(
                builder["frequency"]
                * LFNoise2.kr(frequency=3).semitones_to_ratio()
                * multiplier
            )
            widths.append(LFNoise2.kr(frequency=3).range(0.3, 0.7))
        source = Pulse.ar(frequency=frequencies, width=widths)
        # source = Splay.ar(source=source)
        for _ in range(3):
            source = LPF.ar(source=source, frequency=builder["filter_frequency"])
        source *= Envelope.asr(attack_time=3, sustain=1, release_time=3, curve=-4).ar(
            done_action="FREE_SYNTH", gate=builder["gate"]
        )
        source = Balance2.ar(
            left=source[0],
            right=source[1],
            position=builder["pan"],
            level=builder["amplitude"],
        )
        Out.ar(source=source, bus=builder["out"])

    synthdef = builder.build(name="pad")
    return synthdef


pad = _build_synthdef()

__all__ = ["pad"]
