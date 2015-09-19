# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def test_SynthDefCompiler_width_first_01():

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


def test_SynthDefCompiler_width_first_02():

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
    sc_synthdef = synthdeftools.SynthDefDecompiler.decompile_synthdef(
        sc_compiled_synthdef)

    assert tuple(repr(_) for _ in sc_synthdef.ugens) == (
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

    assert str(py_synthdef) == stringtools.normalize(r'''
        SynthDef PVCopyTest {
            const_0:2.0 -> 1_MaxLocalBufs[0:maximum]
            const_1:1.0 -> 2_LocalBuf[0:channel_count]
            const_2:2048.0 -> 2_LocalBuf[1:frame_count]
            1_MaxLocalBufs[0] -> 2_LocalBuf[2]
            2_LocalBuf[0] -> 3_FFT[0:buffer_id]
            0_PinkNoise[0] -> 3_FFT[1:source]
            const_3:0.5 -> 3_FFT[2:hop]
            const_4:0.0 -> 3_FFT[3:window_type]
            const_1:1.0 -> 3_FFT[4:active]
            const_4:0.0 -> 3_FFT[5:window_size]
            2_LocalBuf[0] -> 4_BufFrames[0:buffer_id]
            const_1:1.0 -> 5_LocalBuf[0:channel_count]
            4_BufFrames[0] -> 5_LocalBuf[1:frame_count]
            1_MaxLocalBufs[0] -> 5_LocalBuf[2]
            3_FFT[0] -> 6_PV_Copy[0:pv_chain_a]
            5_LocalBuf[0] -> 6_PV_Copy[1:pv_chain_b]
            6_PV_Copy[0] -> 7_PV_BinScramble[0:pv_chain]
            const_4:0.0 -> 7_PV_BinScramble[1:wipe]
            const_5:0.2 -> 7_PV_BinScramble[2:width]
            const_4:0.0 -> 7_PV_BinScramble[3:trigger]
            3_FFT[0] -> 8_PV_MagFreeze[0:pv_chain]
            const_4:0.0 -> 8_PV_MagFreeze[1:freeze]
            7_PV_BinScramble[0] -> 9_PV_MagMul[0:pv_chain_a]
            8_PV_MagFreeze[0] -> 9_PV_MagMul[1:pv_chain_b]
            9_PV_MagMul[0] -> 10_IFFT[0:pv_chain]
            const_4:0.0 -> 10_IFFT[1:window_type]
            const_4:0.0 -> 10_IFFT[2:window_size]
            const_4:0.0 -> 11_Out[0:bus]
            10_IFFT[0] -> 11_Out[1:source]
        }
        ''')
    assert str(sc_synthdef) == stringtools.normalize(r'''
        SynthDef PVCopyTest {
            const_0:2.0 -> 1_MaxLocalBufs[0:maximum]
            const_1:1.0 -> 2_LocalBuf[0:channel_count]
            const_2:2048.0 -> 2_LocalBuf[1:frame_count]
            1_MaxLocalBufs[0] -> 2_LocalBuf[2]
            2_LocalBuf[0] -> 3_FFT[0:buffer_id]
            0_PinkNoise[0] -> 3_FFT[1:source]
            const_3:0.5 -> 3_FFT[2:hop]
            const_4:0.0 -> 3_FFT[3:window_type]
            const_1:1.0 -> 3_FFT[4:active]
            const_4:0.0 -> 3_FFT[5:window_size]
            2_LocalBuf[0] -> 4_BufFrames[0:buffer_id]
            const_1:1.0 -> 5_LocalBuf[0:channel_count]
            4_BufFrames[0] -> 5_LocalBuf[1:frame_count]
            1_MaxLocalBufs[0] -> 5_LocalBuf[2]
            3_FFT[0] -> 6_PV_Copy[0:pv_chain_a]
            5_LocalBuf[0] -> 6_PV_Copy[1:pv_chain_b]
            6_PV_Copy[0] -> 7_PV_BinScramble[0:pv_chain]
            const_4:0.0 -> 7_PV_BinScramble[1:wipe]
            const_5:0.20000000298 -> 7_PV_BinScramble[2:width]
            const_4:0.0 -> 7_PV_BinScramble[3:trigger]
            3_FFT[0] -> 8_PV_MagFreeze[0:pv_chain]
            const_4:0.0 -> 8_PV_MagFreeze[1:freeze]
            7_PV_BinScramble[0] -> 9_PV_MagMul[0:pv_chain_a]
            8_PV_MagFreeze[0] -> 9_PV_MagMul[1:pv_chain_b]
            9_PV_MagMul[0] -> 10_IFFT[0:pv_chain]
            const_4:0.0 -> 10_IFFT[1:window_type]
            const_4:0.0 -> 10_IFFT[2:window_size]
            const_4:0.0 -> 11_Out[0:bus]
            10_IFFT[0] -> 11_Out[1:source]
        }
        ''')
    assert tuple(repr(_) for _ in sc_synthdef.ugens) == \
        tuple(repr(_) for _ in py_synthdef.ugens)

    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\nPVCopyTest'
                b'\x00\x00\x00\x06'
                    b'@\x00\x00\x00'
                    b'?\x80\x00\x00'
                    b'E\x00\x00\x00'
                    b'?\x00\x00\x00'
                    b'\x00\x00\x00\x00'
                    b'>L\xcc\xcd'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x0c'
                    b'\tPinkNoise'
                        b'\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x02'
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
                                b'\x00\x00\x00\x01'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00'
                            b'\x00'
                    b'\x03FFT'
                        b'\x01'
                        b'\x00\x00\x00\x06'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x03'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x04'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x04'
                            b'\x01'
                    b'\tBufFrames'
                        b'\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x00'
                            b'\x00'
                    b'\x08LocalBuf'
                        b'\x00'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x04'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00'
                            b'\x00'
                    b'\x07PV_Copy'
                        b'\x01'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x05'
                                b'\x00\x00\x00\x00'
                            b'\x01'
                    b'\x0ePV_BinScramble'
                        b'\x01'
                        b'\x00\x00\x00\x04'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x06'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x04'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x05'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x04'
                            b'\x01'
                    b'\x0cPV_MagFreeze'
                        b'\x01'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x04'
                            b'\x01'
                    b'\tPV_MagMul'
                        b'\x01'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x07'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x08'
                                b'\x00\x00\x00\x00'
                            b'\x01'
                    b'\x04IFFT'
                        b'\x02'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\t'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x04'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x04'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff\x00\x00\x00\x04\x00\x00\x00\n\x00\x00\x00\x00'
                b'\x00\x00'
        )

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef