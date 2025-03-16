from supriya.ugens import (
    Decay2,
    DelayC,
    In,
    Mix,
    Out,
    Parameter,
    SinOsc,
    SynthDefBuilder,
    decompile_synthdef,
)


def test_SynthDefDecompiler_01() -> None:
    r"""Anonymous SynthDef without parameters."""
    with SynthDefBuilder() as builder:
        sine = SinOsc.ar()
        sine = -sine
        Out.ar(bus=99, source=sine)
    old_synthdef = builder.build()
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_02() -> None:
    r"""Anonymous SynthDef with one parameter."""
    with SynthDefBuilder(freq=440) as builder:
        sine = SinOsc.ar(frequency=builder["freq"])
        Out.ar(bus=0, source=sine)
    old_synthdef = builder.build()
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_03() -> None:
    r"""Named SynthDef with one parameter."""
    with SynthDefBuilder(freq=440) as builder:
        sine = SinOsc.ar(frequency=builder["freq"])
        Out.ar(bus=0, source=sine)
    old_synthdef = builder.build("test")
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_04() -> None:
    r"""Multiple parameters."""
    with SynthDefBuilder(freq=1200, out=23) as builder:
        sine = SinOsc.ar(frequency=builder["freq"])
        Out.ar(bus=builder["out"], source=sine)
    old_synthdef = builder.build("test")
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_05() -> None:
    """Multiple parameters."""
    builder = SynthDefBuilder(damping=0.5, delay_time=1.0, room_size=0.75)
    with builder:
        microphone = In.ar(bus=0)
        delay = DelayC.ar(
            source=microphone, maximum_delay_time=5.0, delay_time=builder["delay_time"]
        )
        Out.ar(bus=0, source=delay)
    old_synthdef = builder.build("test")
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_06() -> None:
    r"""Multiple parameters with different rates."""
    builder = SynthDefBuilder(
        a_phase=0.0, freq=440, i_decay_time=1.0, t_trig_a=0, t_trig_b=0
    )
    with builder:
        decay = Decay2.kr(
            source=(builder["t_trig_a"], builder["t_trig_b"]),
            attack_time=0.5,
            decay_time=builder["i_decay_time"],
        )
        sin_osc = SinOsc.ar(frequency=builder["freq"], phase=builder["a_phase"])
        enveloped_sin_osc = sin_osc * decay
        Out.ar(bus=0, source=enveloped_sin_osc)
    old_synthdef = builder.build("trigTest")
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_07() -> None:
    builder = SynthDefBuilder(amp=0.5, freqs=[300, 400])
    with builder:
        sines = SinOsc.ar(frequency=builder["freqs"])
        sines = Mix.new(sines)
        sines = sines * builder["amp"]
        Out.ar(bus=0, source=sines)
    old_synthdef = builder.build("arrayarg")
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_08() -> None:
    r"""Multiple parameters with different lags."""
    builder = SynthDefBuilder(amp=0.5, freqs=Parameter(lag=0.5, value=[300, 400]))
    with builder:
        sines = SinOsc.ar(frequency=builder["freqs"])
        sines = Mix.new(sines)
        sines = sines * builder["amp"]
        Out.ar(bus=0, source=sines)
    old_synthdef = builder.build("arrayarg")
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name
