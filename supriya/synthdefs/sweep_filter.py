from supriya.tools import synthdeftools
from supriya.tools import ugentools


def _build_synthdef():

    builder = synthdeftools.SynthDefBuilder(
        bus=0,
        cutoff=0.5,
        )
    with builder:
        source = ugentools.In.ar(bus=builder['bus'])
        cutoff = builder['cutoff']
        cutoff = ugentools.Lag.kr(source=cutoff)
        lpf_cutoff = cutoff.clip(0., 0.75)
        lpf_frequency = lpf_cutoff.scale(0, 0.75, 20, 22000, True)
        hpf_cutoff = cutoff.clip(0.25, 1.0)
        hpf_frequency = hpf_cutoff.scale(0.25, 1.0, 20, 22000, True)
        source = ugentools.LPF.ar(
            source=source,
            frequency=lpf_frequency,
            )
        source = ugentools.HPF.ar(
            source=source,
            frequency=hpf_frequency,
            )
        ugentools.ReplaceOut.ar(
            bus=builder['bus'],
            source=source,
            )
    synthdef = builder.build()
    return synthdef


sweep_filter = _build_synthdef()

__all__ = (
    'sweep_filter',
    )
