# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools

decompiler = synthdeftools.SynthDefDecompiler


def test_SynthDefDecompiler_01():
    r'''Anonymous SynthDef without parameters.'''
    with synthdeftools.SynthDefBuilder() as builder:
        sine = ugentools.SinOsc.ar()
        sine = -sine
        ugentools.Out.ar(bus=99, source=sine)
    old_synthdef = builder.build()
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_02():
    r'''Anonymous SynthDef with one parameter.'''
    with synthdeftools.SynthDefBuilder(freq=440) as builder:
        sine = ugentools.SinOsc.ar(frequency=builder['freq'])
        ugentools.Out.ar(bus=0, source=sine)
    old_synthdef = builder.build()
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_03():
    r'''Named SynthDef with one parameter.'''
    with synthdeftools.SynthDefBuilder(freq=440) as builder:
        sine = ugentools.SinOsc.ar(frequency=builder['freq'])
        ugentools.Out.ar(bus=0, source=sine)
    old_synthdef = builder.build('test')
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_04():
    r'''Multiple parameters.'''
    with synthdeftools.SynthDefBuilder(freq=1200, out=23) as builder:
        sine = ugentools.SinOsc.ar(frequency=builder['freq'])
        ugentools.Out.ar(bus=builder['out'], source=sine)
    old_synthdef = builder.build('test')
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_05():
    '''Multiple parameters.'''
    builder = synthdeftools.SynthDefBuilder(
        damping=0.5,
        delay_time=1.0,
        room_size=0.75,
        )
    with builder:
        microphone = ugentools.In.ar(bus=0)
        delay = ugentools.DelayC.ar(
            source=microphone,
            maximum_delay_time=5.0,
            delay_time=builder['delay_time'],
            )
        ugentools.Out.ar(bus=0, source=delay)
    old_synthdef = builder.build('test')
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_06():
    r'''Multiple parameters with different rates.'''
    builder = synthdeftools.SynthDefBuilder(
        a_phase=0.0,
        freq=440,
        i_decay_time=1.0,
        t_trig_a=0,
        t_trig_b=0,
        )
    with builder:
        decay = ugentools.Decay2.kr(
            source=(builder['t_trig_a'], builder['t_trig_b']),
            attack_time=0.5,
            decay_time=builder['i_decay_time'],
            )
        sin_osc = ugentools.SinOsc.ar(
            frequency=builder['freq'],
            phase=builder['a_phase'],
            )
        enveloped_sin_osc = sin_osc * decay
        ugentools.Out.ar(
            bus=0,
            source=enveloped_sin_osc,
            )
    old_synthdef = builder.build('trigTest')
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_07():
    builder = synthdeftools.SynthDefBuilder(
        amp=0.5,
        freqs=[300, 400],
        )
    with builder:
        sines = ugentools.SinOsc.ar(
            frequency=builder['freqs'],
            )
        sines = ugentools.Mix.new(sines)
        sines = sines * builder['amp']
        ugentools.Out.ar(
            bus=0,
            source=sines,
            )
    old_synthdef = builder.build('arrayarg')
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name


def test_SynthDefDecompiler_08():
    r'''Multiple parameters with different lags.'''
    builder = synthdeftools.SynthDefBuilder(
        amp=0.5,
        freqs=synthdeftools.Parameter(
            lag=0.5,
            value=[300, 400],
            ),
        )
    with builder:
        sines = ugentools.SinOsc.ar(
            frequency=builder['freqs'],
            )
        sines = ugentools.Mix.new(sines)
        sines = sines * builder['amp']
        ugentools.Out.ar(
            bus=0,
            source=sines,
            )
    old_synthdef = builder.build('arrayarg')
    compiled_synthdef = old_synthdef.compile()
    new_synthdef = decompiler.decompile_synthdef(compiled_synthdef)
    assert str(old_synthdef) == str(new_synthdef)
    assert old_synthdef.indexed_parameters == new_synthdef.indexed_parameters
    assert compiled_synthdef == new_synthdef.compile()
    assert old_synthdef.anonymous_name == new_synthdef.anonymous_name
    assert old_synthdef.name == new_synthdef.name
