# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def test_SynthDef_width_first_01():

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


def test_SynthDef_width_first_02():

    with synthdeftools.SynthDefBuilder() as builder:
        source = ugentools.PinkNoise.ar()
        local_buf = ugentools.LocalBuf(2048)
        pv_chain = ugentools.FFT(buffer_id=local_buf, source=source)
        pv_chain_a = ugentools.PV_BinScramble(pv_chain=pv_chain)
        pv_chain_b = ugentools.PV_MagFreeze(pv_chain=pv_chain)
        pv_chain = ugentools.PV_MagMul(pv_chain_a, pv_chain_b)
        ifft = ugentools.IFFT.ar(pv_chain=pv_chain)
        ugentools.Out.ar(bus=0, source=ifft)
    py_synthdef = builder.build('PVCopyTest')
    py_compiled_synthdef = py_synthdef.compile()

    assert tuple(repr(_) for _ in py_synthdef.ugens) == (
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

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'PVCopyTest',
        r'''
        var source, pv_chain, pv_chain_a, pv_chain_b, ifft, out;
        source = PinkNoise.ar();
        pv_chain = FFT(LocalBuf(2048), source);
        pv_chain_a = PV_BinScramble(pv_chain);
        pv_chain_b = PV_MagFreeze(pv_chain);
        pv_chain = PV_MagMul(pv_chain_a, pv_chain_b);
        ifft = IFFT.ar(pv_chain);
        out = Out.ar(0, ifft);
        '''
        )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())

    assert sc_compiled_synthdef == py_compiled_synthdef

