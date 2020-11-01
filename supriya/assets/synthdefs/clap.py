import supriya.synthdefs
import supriya.ugens

"""
SynthDef("clap", {
    arg outBus=0, amp = 0.5;
    var env1, env2, out, noise1, noise2;

    env1 = EnvGen.ar(
        Env.new(
            [0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0.001, 0.013, 0, 0.01, 0, 0.01, 0, 0.03],
            [0, -3, 0, -3, 0, -3, 0, -4],
            )
        );
    env2 = EnvGen.ar(
        Env.new(
            [0, 1, 0],
            [0.02, 0.3],
            [0, -4]
            ),
        doneAction:2,
        );

    noise1 = WhiteNoise.ar(env1);
    noise1 = HPF.ar(noise1, 600);
    noise1 = BPF.ar(noise1, 2000, 3);

    noise2 = WhiteNoise.ar(env2);
    noise2 = HPF.ar(noise2, 1000);
    noise2 = BPF.ar(noise2, 1200, 0.7, 0.7);

    out = noise1 + noise2;
    out = out * 2;
    out = out.softclip * amp;

    Out.ar(outBus, out.dup);
})
"""


def _build_clap_synthdef():

    with supriya.synthdefs.SynthDefBuilder(out=0, amplitude=0.5) as builder:

        envelope_one = supriya.synthdefs.Envelope(
            amplitudes=(0, 1, 0, 1, 0, 1, 0, 1, 0),
            durations=(0.001, 0.013, 0, 0.01, 0, 0.01, 0, 0.03),
            curves=(0, -3, 0, -3, 0, -3, 0, -4),
        )
        envelope_generator_one = supriya.ugens.EnvGen.ar(envelope=envelope_one)

        envelope_two = supriya.synthdefs.Envelope(
            amplitudes=(0, 1, 0), durations=(0.02, 0.3), curves=(0, -4)
        )
        envelope_generator_two = supriya.ugens.EnvGen.ar(
            envelope=envelope_two, done_action=2
        )

        noise_one = supriya.ugens.WhiteNoise.ar() * envelope_generator_one
        noise_one = supriya.ugens.HPF.ar(source=noise_one, frequency=600)
        noise_one = supriya.ugens.BPF.ar(
            source=noise_one, frequency=2000, reciprocal_of_q=3
        )

        noise_two = supriya.ugens.WhiteNoise.ar() * envelope_generator_two
        noise_two = supriya.ugens.HPF.ar(source=noise_two, frequency=1000)
        noise_two = supriya.ugens.BPF.ar(
            source=noise_two, frequency=1200, reciprocal_of_q=0.7
        )
        noise_two = noise_two * 0.7

        result = noise_one + noise_two
        result = result * 2
        result = result.softclip()
        result = result * builder["amplitude"]

        supriya.ugens.Out.ar(bus=builder["out"], source=(result, result))

    synthdef = builder.build()
    return synthdef


clap = _build_clap_synthdef()

__all__ = ("clap",)
