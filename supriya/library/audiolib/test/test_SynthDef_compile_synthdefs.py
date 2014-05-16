# -*- encoding: utf-8 -*-
from supriya import audiolib


def test_SynthDef_compile_synthdefs_01():

    sc_synthdef = audiolib.SCSynthDef(
        'foo',
        'Out.ar(0, SinOsc.ar(freq: 420) * SinOsc.ar(freq: 440))',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = audiolib.SynthDef('foo')
    sine_one = audiolib.SinOsc.ar(freq=420)
    sine_two = audiolib.SinOsc.ar(freq=440)
    sines = sine_one * sine_two
    out = audiolib.Out.ar(bus=0, source=sines)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = (
        'SCgf'
        '\x00\x00\x00\x02'
        '\x00\x01'
            '\x03foo'
                '\x00\x00\x00\x03'
                    'C\xd2\x00\x00'
                    '\x00\x00\x00\x00'
                    'C\xdc\x00\x00'
                '\x00\x00\x00\x00'
                '\x00\x00\x00\x00'
                '\x00\x00\x00\x04'
                    '\x06SinOsc'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x01'
                        '\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x01'
                            '\x02'
                    '\x06SinOsc'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x01'
                        '\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x02'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x01'
                            '\x02'
                    '\x0cBinaryOpUGen'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x01'
                        '\x00\x02'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x01'
                            '\x00\x00\x00\x00'
                            '\x02'
                    '\x03Out'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x00'
                        '\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x01'
                            '\x00\x00\x00\x02'
                            '\x00\x00\x00\x00'
                '\x00\x00'
        )

    assert py_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == sc_compiled_synthdef


def test_SynthDef_compile_synthdefs_02():

    sc_synthdef = audiolib.SCSynthDef(
        'test',
        'Out.ar(99, SinOsc.ar(freq: 440).neg)',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = audiolib.SynthDef('test')
    sine = audiolib.SinOsc.ar()
    sine = -sine
    out = audiolib.Out.ar(bus=99, source=sine)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = (
        'SCgf'
        '\x00\x00\x00\x02'
        '\x00\x01'
            '\x04test'
                '\x00\x00\x00\x03'
                    'C\xdc\x00\x00'
                    '\x00\x00\x00\x00'
                    'B\xc6\x00\x00'
                '\x00\x00\x00\x00'
                '\x00\x00\x00\x00'
                '\x00\x00\x00\x03'
                    '\x06SinOsc'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x01'
                        '\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x01'
                            '\x02'
                    '\x0bUnaryOpUGen'
                        '\x02'
                        '\x00\x00\x00\x01'
                        '\x00\x00\x00\x01'
                        '\x00\x00'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x00'
                            '\x02'
                    '\x03Out'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x00'
                        '\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x02'
                            '\x00\x00\x00\x01'
                            '\x00\x00\x00\x00'
                    '\x00\x00'
        )

    assert py_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == sc_compiled_synthdef



def test_SynthDef_compile_synthdefs_03():

    sc_synthdef = audiolib.SCSynthDef(
        'test',
        r'''
        arg freq=1200, out=23;
        Out.ar(out, SinOsc.ar(freq: freq));
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = audiolib.SynthDef('test', freq=1200, out=23)
    controls = py_synthdef.controls
    sine = audiolib.SinOsc.ar(freq=controls['freq'])
    out = audiolib.Out.ar(bus=controls['out'], source=sine)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = (
        'SCgf'
        '\x00\x00\x00\x02'
        '\x00\x01'
            '\x04test'
                '\x00\x00\x00\x01'
                    '\x00\x00\x00\x00'
                '\x00\x00\x00\x02'
                    'D\x96\x00\x00'
                    'A\xb8\x00\x00'
                '\x00\x00\x00\x02'
                    '\x04freq'
                    '\x00\x00\x00\x00'
                    '\x03out'
                    '\x00\x00\x00\x01'
                '\x00\x00\x00\x03'
                    '\x07Control'
                        '\x01'
                        '\x00\x00\x00\x00'
                        '\x00\x00\x00\x02'
                        '\x00\x00'
                        '\x01'
                        '\x01'
                    '\x06SinOsc'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x01'
                        '\x00\x00'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x00'
                            '\x02'
                    '\x03Out'
                        '\x02'
                        '\x00\x00\x00\x02'
                        '\x00\x00\x00\x00'
                        '\x00\x00'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x01'
                            '\x00\x00\x00\x01'
                            '\x00\x00\x00\x00'
                '\x00\x00'
        )

    assert py_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == sc_compiled_synthdef


def test_SynthDef_compile_synthdefs_04():

    sc_synthdef = audiolib.SCSynthDef(
        'test',
        r'''
        Out.ar(0, In.ar(8, 2))
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = audiolib.SynthDef('test')
    inputs = audiolib.In.ar(bus=8, channel_count=2)
    out = audiolib.Out.ar(bus=0, source=inputs)
    py_synthdef.add_ugen(out)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = (
        'SCgf'
        '\x00\x00\x00\x02'
        '\x00\x01'
            '\x04test'
                '\x00\x00\x00\x02'
                    'A\x00\x00\x00'
                    '\x00\x00\x00\x00'
                '\x00\x00\x00\x00'
                '\x00\x00\x00\x00'
                '\x00\x00\x00\x02'
                    '\x02In'
                        '\x02'
                        '\x00\x00\x00\x01'
                        '\x00\x00\x00\x02'
                        '\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x00'
                            '\x02'
                            '\x02'
                    '\x03Out'
                        '\x02'
                        '\x00\x00\x00\x03'
                        '\x00\x00\x00\x00'
                        '\x00\x00'
                            '\xff\xff\xff\xff'
                            '\x00\x00\x00\x01'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x00'
                            '\x00\x00\x00\x01'
                '\x00\x00'
        )

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == sc_compiled_synthdef
