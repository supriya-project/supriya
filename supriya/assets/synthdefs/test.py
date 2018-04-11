from supriya.tools import synthdeftools
import supriya.ugens


def _build_test_synthdef():
    with synthdeftools.SynthDefBuilder(
        frequency=440,
        amplitude=synthdeftools.Parameter(
            value=1.0,
            parameter_rate=synthdeftools.ParameterRate.AUDIO,
            ),
        ) as builder:
        sin_osc = supriya.ugens.SinOsc.ar(frequency=builder['frequency'])
        enveloped_sin = sin_osc * builder['amplitude']
        supriya.ugens.Out.ar(bus=0, source=enveloped_sin)
    synthdef = builder.build(name='test')
    return synthdef


test = _build_test_synthdef()

__all__ = (
    'test',
    )
