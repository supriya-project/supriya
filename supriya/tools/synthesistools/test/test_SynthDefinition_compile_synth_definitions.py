# -*- encoding: utf-8 -*-
from supriya import synthesistools


def test_SynthDefinition_compile_synth_definitions_01():

    sc_synth_definition = synthesistools.SuperColliderSynthDefinition(
        'foo',
        'Out.ar(0, SinOsc.ar(freq: 420) * SinOsc.ar(freq: 440))',
        )
    sc_compiled_synth_definition = sc_synth_definition.compile()

    py_synth_definition = synthesistools.SynthDefinition('foo')
    sine_one = synthesistools.SinOsc.ar(frequency=420)
    sine_two = synthesistools.SinOsc.ar(frequency=440)
    sines = sine_one * sine_two
    out = synthesistools.Out.ar(bus=0, source=sines)
    py_synth_definition.add_ugen(out)
    py_compiled_synth_definition = py_synth_definition.compile()

    test_compiled_synth_definition = bytearray(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x03foo'
                b'\x00\x00\x00\x03'
                    b'C\xd2\x00\x00'
                    b'\x00\x00\x00\x00'
                    b'C\xdc\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x04'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x02'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x02'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x02'
                    b'\x0cBinaryOpUGen'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x02'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x00'
                b'\x00\x00',
        )

    assert sc_compiled_synth_definition == test_compiled_synth_definition
    assert py_compiled_synth_definition == test_compiled_synth_definition


def test_SynthDefinition_compile_synth_definitions_02():

    sc_synth_definition = synthesistools.SuperColliderSynthDefinition(
        'test',
        'Out.ar(99, SinOsc.ar(freq: 440).neg)',
        )
    sc_compiled_synth_definition = sc_synth_definition.compile()

    py_synth_definition = synthesistools.SynthDefinition('test')
    sine = synthesistools.SinOsc.ar()
    sine = -sine
    out = synthesistools.Out.ar(bus=99, source=sine)
    py_synth_definition.add_ugen(out)
    py_compiled_synth_definition = py_synth_definition.compile()

    test_compiled_synth_definition = bytearray(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x04test'
                b'\x00\x00\x00\x03'
                    b'C\xdc\x00\x00'
                    b'\x00\x00\x00\x00'
                    b'B\xc6\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x03'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x02'
                    b'\x0bUnaryOpUGen'
                        b'\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                b'\x00\x00',
        )

    assert sc_compiled_synth_definition == test_compiled_synth_definition
    assert py_compiled_synth_definition == test_compiled_synth_definition



def test_SynthDefinition_compile_synth_definitions_03():

    sc_synth_definition = synthesistools.SuperColliderSynthDefinition(
        'test',
        r'''
        arg freq=1200, out=23;
        Out.ar(out, SinOsc.ar(freq: freq));
        '''
        )
    sc_compiled_synth_definition = sc_synth_definition.compile()

    py_synth_definition = synthesistools.SynthDefinition('test', freq=1200, out=23)
    controls = py_synth_definition.controls
    sine = synthesistools.SinOsc.ar(frequency=controls['freq'])
    out = synthesistools.Out.ar(bus=controls['out'], source=sine)
    py_synth_definition.add_ugen(out)
    py_compiled_synth_definition = py_synth_definition.compile()

    test_compiled_synth_definition = bytearray(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x04test'
                b'\x00\x00\x00\x01'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x02'
                    b'D\x96\x00\x00'
                    b'A\xb8\x00\x00'
                b'\x00\x00\x00\x02'
                    b'\x04freq'
                    b'\x00\x00\x00\x00'
                    b'\x03out'
                    b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x03'
                    b'\x07Control'
                        b'\x01'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00'
                        b'\x01'
                        b'\x01'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                b'\x00\x00',
        )

    assert sc_compiled_synth_definition == test_compiled_synth_definition
    assert py_compiled_synth_definition == test_compiled_synth_definition


def test_SynthDefinition_compile_synth_definitions_04():

    sc_synth_definition = synthesistools.SuperColliderSynthDefinition(
        'test',
        r'''
        Out.ar(0, In.ar(8, 2))
        '''
        )
    sc_compiled_synth_definition = sc_synth_definition.compile()

    py_synth_definition = synthesistools.SynthDefinition('test')
    inputs = synthesistools.In.ar(bus=8, channel_count=2)
    out = synthesistools.Out.ar(bus=0, source=inputs)
    py_synth_definition.add_ugen(out)
    py_compiled_synth_definition = py_synth_definition.compile()

    test_compiled_synth_definition = bytearray(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x04test'
                b'\x00\x00\x00\x02'
                    b'A\x00\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x02'
                    b'\x02In'
                        b'\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x02'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                b'\x00\x00',
        )

    assert sc_compiled_synth_definition == test_compiled_synth_definition
    assert py_compiled_synth_definition == test_compiled_synth_definition


def test_SynthDefinition_compile_synth_definitions_05():

    sc_synth_definition = synthesistools.SuperColliderSynthDefinition(
        'test',
        r'''
        | freq = 440 | Out.ar(0, SinOsc.ar(freq))
        '''
        )
    sc_compiled_synth_definition = sc_synth_definition.compile()

    py_synth_definition = synthesistools.SynthDefinition('test', freq=440)
    controls = py_synth_definition.controls
    sine = synthesistools.SinOsc.ar(frequency=controls['freq'])
    out = synthesistools.Out.ar(bus=0, source=sine)
    py_synth_definition.add_ugen(out)
    py_compiled_synth_definition = py_synth_definition.compile()

    test_compiled_synth_definition = bytearray(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x04test'
                b'\x00\x00\x00\x01'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x01'
                    b'C\xdc\x00\x00'
                b'\x00\x00\x00\x01'
                    b'\x04freq'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x03'
                    b'\x07Control'
                        b'\x01'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x01'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                b'\x00\x00',
        )

    assert sc_compiled_synth_definition == test_compiled_synth_definition
    assert py_compiled_synth_definition == test_compiled_synth_definition


def test_SynthDefinition_compile_synth_definitions_06():
    r'''Multiple parameters, including unused parameters.
    '''

    sc_synth_definition = synthesistools.SuperColliderSynthDefinition(
        'test',
        r'''
        | damping=0.1, delay_time=1.0, room_size=0.9 |
        Out.ar(0, DelayC.ar(In.ar(0), 5.0, delay_time))
        '''
        )
    sc_compiled_synth_definition = sc_synth_definition.compile()

    py_synth_definition = synthesistools.SynthDefinition(
        'test',
        damping=0.1,
        delay_time=1.0,
        room_size=0.9,
        )
    controls = py_synth_definition.controls
    microphone = synthesistools.In.ar(bus=0)
    delay = synthesistools.DelayC.ar(
        source=microphone,
        maximum_delay_time=5.0,
        delay_time=controls['delay_time'],
        )
    out = synthesistools.Out.ar(bus=0, source=delay)
    py_synth_definition.add_ugen(out)
    py_compiled_synth_definition = py_synth_definition.compile()

    test_compiled_synth_definition = bytearray(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x04test'
                b'\x00\x00\x00\x02'
                    b'\x00\x00\x00\x00'
                    b'@\xa0\x00\x00'
                b'\x00\x00\x00\x03'
                    b'=\xcc\xcc\xcd'
                    b'?\x80\x00\x00'
                    b'?fff'
                b'\x00\x00\x00\x03'
                    b'\x07damping'
                    b'\x00\x00\x00\x00'
                    b'\ndelay_time'
                    b'\x00\x00\x00\x01'
                    b'\x09room_size'
                    b'\x00\x00\x00\x02'
                b'\x00\x00\x00\x04'
                    b'\x07Control'
                        b'\x01'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00'
                            b'\x01'
                            b'\x01'
                            b'\x01'
                    b'\x02In'
                        b'\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x06DelayC'
                        b'\x02'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x00'
                b'\x00\x00',
        )

    assert len(py_compiled_synth_definition) == len(test_compiled_synth_definition)
    for i in range(len(py_compiled_synth_definition)):
        assert py_compiled_synth_definition[i] == test_compiled_synth_definition[i], (
            i, py_compiled_synth_definition[i], test_compiled_synth_definition[i])

    assert sc_compiled_synth_definition == test_compiled_synth_definition
    assert py_compiled_synth_definition == test_compiled_synth_definition
