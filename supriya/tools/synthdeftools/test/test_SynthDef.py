# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def test_SynthDef_01():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'foo',
        'Out.ar(0, SinOsc.ar(freq: 420) * SinOsc.ar(freq: 440))',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    builder = synthdeftools.SynthDefBuilder()
    sine_one = ugentools.SinOsc.ar(frequency=420)
    sine_two = ugentools.SinOsc.ar(frequency=440)
    sines = sine_one * sine_two
    out = ugentools.Out.ar(bus=0, source=sines)
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
    assert py_compiled_synthdef_new == test_compiled_synthdef


def test_SynthDef_02():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        'Out.ar(99, SinOsc.ar(freq: 440).neg)',
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    builder = synthdeftools.SynthDefBuilder()
    sine = ugentools.SinOsc.ar()
    sine = -sine
    out = ugentools.Out.ar(bus=99, source=sine)
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

    builder = synthdeftools.SynthDefBuilder(
        freq=1200,
        out=23,
        )
    sine = ugentools.SinOsc.ar(frequency=builder['freq'])
    out = ugentools.Out.ar(bus=builder['out'], source=sine)
    builder.add_ugen(out)
    py_synthdef_new = builder.build('test')
    py_compiled_synthdef_new = py_synthdef_new.compile()

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
    assert py_compiled_synthdef_new == test_compiled_synthdef


def test_SynthDef_04():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        r'''
        Out.ar(0, In.ar(8, 2))
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    builder = synthdeftools.SynthDefBuilder()
    inputs = ugentools.In.ar(bus=8, channel_count=2)
    out = ugentools.Out.ar(bus=0, source=inputs)
    builder.add_ugen(out)
    py_synthdef_new = builder.build('test')
    py_compiled_synthdef_new = py_synthdef_new.compile()

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
    assert py_compiled_synthdef_new == test_compiled_synthdef


def test_SynthDef_05():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'test',
        r'''
        | freq = 440 |
        Out.ar(0, SinOsc.ar(freq: freq))
        '''
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    builder = synthdeftools.SynthDefBuilder(freq=440)
    sine = ugentools.SinOsc.ar(frequency=builder['freq'])
    out = ugentools.Out.ar(bus=0, source=sine)
    builder.add_ugen(out)
    py_synthdef_new = builder.build('test')
    py_compiled_synthdef_new = py_synthdef_new.compile()

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
    assert py_compiled_synthdef_new == test_compiled_synthdef


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

    builder = synthdeftools.SynthDefBuilder(
        damping=0.1,
        delay_time=1.0,
        room_size=0.9,
        )
    microphone = ugentools.In.ar(bus=0)
    delay = ugentools.DelayC.ar(
        source=microphone,
        maximum_delay_time=5.0,
        delay_time=builder['delay_time'],
        )
    out = ugentools.Out.ar(bus=0, source=delay)
    builder.add_ugen(out)
    py_synthdef_new = builder.build('test')
    py_compiled_synthdef_new = py_synthdef_new.compile()

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

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef_new == test_compiled_synthdef


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

    builder = synthdeftools.SynthDefBuilder()
    sin_osc = ugentools.SinOsc.ar()
    free_self = ugentools.FreeSelf.kr(sin_osc)
    out = ugentools.Out.ar(bus=0, source=sin_osc)
    builder.add_ugen(free_self)
    builder.add_ugen(out)
    py_synthdef_new = builder.build('test')
    py_compiled_synthdef_new = py_synthdef_new.compile()

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

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef_new == test_compiled_synthdef


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

    builder = synthdeftools.SynthDefBuilder(
        a_phase=0.0,
        freq=440,
        i_decay_time=1.0,
        t_trig_a=0,
        t_trig_b=0,
        )
    decay = ugentools.Decay2.kr(
        source=(builder['t_trig_a'], builder['t_trig_b']),
        attack_time=0.005,
        decay_time=builder['i_decay_time'],
        )
    sin_osc = ugentools.SinOsc.ar(
        frequency=builder['freq'],
        phase=builder['a_phase'],
        )
    enveloped_sin_osc = sin_osc * decay
    out = ugentools.Out.ar(
        bus=0,
        source=enveloped_sin_osc,
        )
    builder.add_ugen(out)
    py_synthdef_new = builder.build('trigTest')
    py_compiled_synthdef_new = py_synthdef_new.compile()

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
    assert py_compiled_synthdef_new == test_compiled_synthdef


def test_SynthDef_09():

    with synthdeftools.SynthDefBuilder() as builder:
        local_buf = ugentools.LocalBuf(2048)
        source = ugentools.PinkNoise.ar()
        pv_chain = ugentools.FFT(
            buffer_id=local_buf,
            source=source,
            )
        ifft = ugentools.IFFT.ar(pv_chain=pv_chain)
        ugentools.Out.ar(bus=0, source=ifft)

    synthdef = builder.build('LocalBufTest')
    py_compiled_synthdef = synthdef.compile()

    test_compiled_synthdef = (
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x0cLocalBufTest'
                b'\x00\x00\x00\x04'
                    b'?\x80\x00\x00'
                    b'E\x00\x00\x00'
                    b'?\x00\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x06'
                    b'\x0cMaxLocalBufs'
                        b'\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x00'
                    b'\x08LocalBuf'
                        b'\x00'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00'
                    b'\tPinkNoise'
                        b'\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x02'
                    b'\x03FFT'
                        b'\x01'
                        b'\x00\x00\x00\x06'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x02'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x03'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x03'
                            b'\x01'
                    b'\x04IFFT'
                        b'\x02'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x03'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x03'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x04'
                            b'\x00\x00\x00\x00'
                b'\x00\x00'
        )

    assert py_compiled_synthdef == test_compiled_synthdef


def test_SynthDef_10():

    with synthdeftools.SynthDefBuilder() as builder:
        source = ugentools.PinkNoise.ar()
        pv_chain = ugentools.FFT(source=source)
        pv_chain_a = ugentools.PV_BinScramble(pv_chain=pv_chain)
        pv_chain_b = ugentools.PV_MagFreeze(pv_chain=pv_chain)
        pv_chain = ugentools.PV_MagMul(pv_chain_a, pv_chain_b)
        ifft = ugentools.IFFT.ar(pv_chain=pv_chain)
        ugentools.Out.ar(bus=0, source=ifft)
    synthdef = builder.build('PVCopyTest')

    assert tuple(repr(_) for _ in synthdef.ugens) == (
        'PinkNoise.ar()',
        'MaxLocalBufs.ir()',
        'LocalBuf.ir()',
        'FFT.kr()',
        'BufFrames.ir()',
        'LocalBuf.ir()',
        'PV_Copy.kr()',
        'PV_BinScramble.kr()',
        'PV_MagFreeze.kr()',
        'PV_MagMul.kr()',
        'IFFT.ar()',
        'Out.ar()',
        )