# -*- encoding: utf-8 -*-
from supriya import synthdefs


def test_SynthDef_compile_synthdefs_01():

    sc_synthdef = synthdefs.SCSynthDef(
        'foo',
        'Out.ar(0, SinOsc.ar(freq: 420) * SinOsc.ar(freq: 440))',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = synthdefs.SynthDef('foo')
    sine_one = synthdefs.SinOsc.ar(freq=420)
    sine_two = synthdefs.SinOsc.ar(freq=440)
    sines = sine_one * sine_two
    out = synthdefs.Out.ar(bus=0, source=sines)
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

    sc_synthdef = synthdefs.SCSynthDef(
        'test',
        'Out.ar(99, SinOsc.ar(freq: 440).neg)',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = synthdefs.SynthDef('test')
    sine = synthdefs.SinOsc.ar()
    sine = -sine
    out = synthdefs.Out.ar(bus=99, source=sine)
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

    sc_synthdef = synthdefs.SCSynthDef(
        'test',
        r'''
        arg freq=1200, out=23;
        Out.ar(out, SinOsc.ar(freq: freq));
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = synthdefs.SynthDef('test', freq=1200, out=23)
    controls = py_synthdef.controls
    sine = synthdefs.SinOsc.ar(freq=controls['freq'])
    out = synthdefs.Out.ar(bus=controls['out'], source=sine)
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
