# -*- encoding: utf-8 -*-
from supriya import synthdefs


def test_SynthDef_compile_synthdefs_01():

    py_synthdef = synthdefs.SynthDef('foo')
    sine_one = synthdefs.SinOsc.ar(freq=420)
    sine_two = synthdefs.SinOsc.ar(freq=440)
    sines = sine_one * sine_two
    out = synthdefs.Out.ar(bus=0, source=sines)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile_synthdefs([py_synthdef])

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

    assert len(py_compiled_synthdef) == len(test_compiled_synthdef)
    assert py_compiled_synthdef == test_compiled_synthdef


def test_SynthDef_compile_synthdefs_02():

    py_synthdef = synthdefs.SynthDef('test')
    sine = synthdefs.SinOsc.ar()
    sine = -sine
    out = synthdefs.Out.ar(bus=99, source=sine)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile_synthdefs([py_synthdef])

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
