from ...ugens import HPF, LPF, In, Lag, ReplaceOut, SynthDef, SynthDefBuilder


def _build_synthdef() -> SynthDef:
    with SynthDefBuilder(bus=0, cutoff=0.5) as builder:
        source = In.ar(bus=builder["bus"])
        cutoff = Lag.kr(source=builder["cutoff"])
        lpf_cutoff = cutoff.clip(0.0, 0.75)
        lpf_frequency = lpf_cutoff.scale(0, 0.75, 20, 22000, True)
        hpf_cutoff = cutoff.clip(0.25, 1.0)
        hpf_frequency = hpf_cutoff.scale(0.25, 1.0, 20, 22000, True)
        source = HPF.ar(
            source=LPF.ar(source=source, frequency=lpf_frequency),
            frequency=hpf_frequency,
        )
        ReplaceOut.ar(bus=builder["bus"], source=source)
    return builder.build(name="sweep_filter")


sweep_filter = _build_synthdef()

__all__ = ["sweep_filter"]
