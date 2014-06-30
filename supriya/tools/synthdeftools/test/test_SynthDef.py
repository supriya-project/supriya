# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def test_SynthDef_01():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'foo',
        'Out.ar(0, SinOsc.ar(freq: 420) * SinOsc.ar(freq: 440))',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef_old = synthdeftools.SynthDef('foo')
    sine_one = ugentools.SinOsc.ar(frequency=420)
    sine_two = ugentools.SinOsc.ar(frequency=440)
    sines = sine_one * sine_two
    out = ugentools.Out.ar(bus=0, source=sines)
    py_synthdef_old.add_ugen(out)
    py_compiled_synthdef_old = py_synthdef_old.compile()

    builder = synthdeftools.SynthDefBuilder()
    builder.add_ugen(out)
    py_synthdef_new = builder.build('foo')
    py_compiled_synthdef_new = py_synthdef_new.compile()

    test_compiled_synthdef = bytes(
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

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef_old == test_compiled_synthdef
    assert py_compiled_synthdef_new == test_compiled_synthdef


def test_SynthDef_02():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        'Out.ar(99, SinOsc.ar(freq: 440).neg)',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef_old = synthdeftools.SynthDef('test')
    sine = ugentools.SinOsc.ar()
    sine = -sine
    out = ugentools.Out.ar(bus=99, source=sine)
    py_synthdef_old.add_ugen(out)
    py_compiled_synthdef_old = py_synthdef_old.compile()

    builder = synthdeftools.SynthDefBuilder()
    builder.add_ugen(out)
    py_synthdef_new = builder.build('test')
    py_compiled_synthdef_new = py_synthdef_new.compile()

    test_compiled_synthdef = bytes(
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

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef_old == test_compiled_synthdef
    assert py_compiled_synthdef_new == test_compiled_synthdef


def test_SynthDef_03():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        r'''
        arg freq=1200, out=23;
        Out.ar(out, SinOsc.ar(freq: freq));
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = synthdeftools.SynthDef('test', freq=1200, out=23)
    controls = py_synthdef.controls
    sine = ugentools.SinOsc.ar(frequency=controls['freq'])
    out = ugentools.Out.ar(bus=controls['out'], source=sine)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = bytes(
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

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef


def test_SynthDef_04():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        r'''
        Out.ar(0, In.ar(8, 2))
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = synthdeftools.SynthDef('test')
    inputs = ugentools.In.ar(bus=8, channel_count=2)
    out = ugentools.Out.ar(bus=0, source=inputs)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = bytes(
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

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef


def test_SynthDef_05():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        r'''
        | freq = 440 | Out.ar(0, SinOsc.ar(freq))
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = synthdeftools.SynthDef('test', freq=440)
    controls = py_synthdef.controls
    sine = ugentools.SinOsc.ar(frequency=controls['freq'])
    out = ugentools.Out.ar(bus=0, source=sine)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = bytes(
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

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef


def test_SynthDef_06():
    r'''Multiple parameters, including unused parameters.
    '''

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        r'''
        | damping=0.1, delay_time=1.0, room_size=0.9 |
        Out.ar(0, DelayC.ar(In.ar(0), 5.0, delay_time))
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    py_synthdef = synthdeftools.SynthDef(
        'test',
        damping=0.1,
        delay_time=1.0,
        room_size=0.9,
        )
    controls = py_synthdef.controls
    microphone = ugentools.In.ar(bus=0)
    delay = ugentools.DelayC.ar(
        source=microphone,
        maximum_delay_time=5.0,
        delay_time=controls['delay_time'],
        )
    out = ugentools.Out.ar(bus=0, source=delay)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = bytes(
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

    assert len(py_compiled_synthdef) == len(test_compiled_synthdef)
    for i in range(len(py_compiled_synthdef)):
        assert py_compiled_synthdef[i] == test_compiled_synthdef[i], (
            i, py_compiled_synthdef[i], test_compiled_synthdef[i])

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef


def test_SynthDef_07():
    r'''FreeSelf.
    '''
    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        r'''
        Out.ar(0, FreeSelf.kr(SinOsc.ar()))
        '''
        )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())

    py_synthdef = synthdeftools.SynthDef('test')
    sin_osc = ugentools.SinOsc.ar()
    free_self = ugentools.FreeSelf.kr(sin_osc)
    out = ugentools.Out.ar(bus=0, source=sin_osc)
    py_synthdef.add_ugen(free_self)
    py_synthdef.add_ugen(out)
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x04test'
                b'\x00\x00\x00\x02'
                    b'C\xdc\x00\x00'
                    b'\x00\x00\x00\x00'
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
                    b'\x08FreeSelf'
                        b'\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x01'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                b'\x00\x00',
        )

    assert len(py_compiled_synthdef) == len(test_compiled_synthdef)
    for i in range(len(py_compiled_synthdef)):
        assert py_compiled_synthdef[i] == test_compiled_synthdef[i], (
            i, py_compiled_synthdef[i], test_compiled_synthdef[i])

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef


def test_SynthDef_08():
    r'''Different calculation rates.'''

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'trigTest',
        r'''
        |
            a_phase = 0.0,
            freq = 440,
            i_decay_time = 1.0,
            t_trig_a = 0,
            t_trig_b = 0
        |
        var decay = Decay2.kr([t_trig_a, t_trig_b], 0.005, i_decay_time);
        Out.ar(0, SinOsc.ar(freq, a_phase) * decay);
        '''
        )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())

    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x08trigTest'
                b'\x00\x00\x00\x02'
                    b';\xa3\xd7\n'
                    b'\x00\x00\x00\x00'
                    b'\x00\x00\x00\x05'
                        b'?\x80\x00\x00'  # i_decay_time
                        b'\x00\x00\x00\x00'  # t_trig_a
                        b'\x00\x00\x00\x00'  # t_trig_b
                        b'\x00\x00\x00\x00'  # a_phase
                        b'C\xdc\x00\x00'  # freq
                    b'\x00\x00\x00\x05'
                        b'\x07a_phase'
                            b'\x00\x00\x00\x03'
                        b'\x04freq'
                            b'\x00\x00\x00\x04'
                        b'\x0ci_decay_time'
                            b'\x00\x00\x00\x00'
                        b'\x08t_trig_a'
                            b'\x00\x00\x00\x01'
                        b'\x08t_trig_b'
                            b'\x00\x00\x00\x02'
                    b'\x00\x00\x00\n'
                        b'\x07Control'
                            b'\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00'
                                b'\x00'
                        b'\x0bTrigControl'
                            b'\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x02'
                            b'\x00\x01'
                                b'\x01'
                                b'\x01'
                        b'\x06Decay2'
                            b'\x01'
                            b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00'
                                b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00'
                                b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                                b'\x01'
                        b'\x06Decay2'
                            b'\x01'
                            b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00'
                                b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x01'
                                b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                                b'\x01'
                        b'\x0cAudioControl'
                            b'\x02'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x03'
                                b'\x02'
                        b'\x07Control'
                            b'\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x04'
                                b'\x01'
                        b'\x06SinOsc'
                            b'\x02'
                            b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00'
                                b'\x00\x00\x00\x05'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x04'
                                b'\x00\x00\x00\x00'
                                b'\x02'
                        b'\x0cBinaryOpUGen'
                            b'\x02'
                            b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x01'
                            b'\x00\x02'
                                b'\x00\x00\x00\x06'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x00'
                                b'\x02'
                        b'\x0cBinaryOpUGen'
                            b'\x02'
                            b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x01'
                            b'\x00\x02'
                                b'\x00\x00\x00\x06'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x00'
                                b'\x02'
                        b'\x03Out'
                            b'\x02'
                            b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00'
                                b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x07'
                                b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x08'
                                b'\x00\x00\x00\x00'
                b'\x00\x00'
        )

    for i, pair in enumerate(zip(sc_compiled_synthdef, test_compiled_synthdef)):
        x, y = pair
        assert x == y, (i, repr(x), repr(y))
    assert sc_compiled_synthdef == test_compiled_synthdef
