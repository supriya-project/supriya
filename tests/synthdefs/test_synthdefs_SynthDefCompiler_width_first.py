# flake8: noqa
import platform

import pytest
from uqbar.strings import normalize

import supriya.synthdefs
import supriya.ugens


def test_01():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        local_buf = supriya.ugens.LocalBuf(2048)
        source = supriya.ugens.PinkNoise.ar()
        pv_chain = supriya.ugens.FFT.kr(buffer_id=local_buf, source=source)
        ifft = supriya.ugens.IFFT.ar(pv_chain=pv_chain)
        supriya.ugens.Out.ar(bus=0, source=ifft)
    py_synthdef = builder.build("LocalBufTest")
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.fixture
def py_synthdef_02():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        source = supriya.ugens.PinkNoise.ar()
        local_buf = supriya.ugens.LocalBuf(2048)
        pv_chain = supriya.ugens.FFT.kr(buffer_id=local_buf, source=source)
        pv_chain_a = supriya.ugens.PV_BinScramble.kr(pv_chain=pv_chain)
        pv_chain_b = supriya.ugens.PV_MagFreeze.kr(pv_chain=pv_chain)
        pv_chain = supriya.ugens.PV_MagMul.kr(
            pv_chain_a=pv_chain_a, pv_chain_b=pv_chain_b
        )
        ifft = supriya.ugens.IFFT.ar(pv_chain=pv_chain)
        supriya.ugens.Out.ar(bus=0, source=ifft)
    py_synthdef = builder.build("PVCopyTest")
    return py_synthdef


def test_02_ugens(py_synthdef_02):
    assert tuple(repr(_) for _ in py_synthdef_02.ugens) == (
        "PinkNoise.ar()",
        "MaxLocalBufs.ir()",
        "LocalBuf.ir()",
        "FFT.kr()",
        "BufFrames.ir()",
        "LocalBuf.ir()",
        "PV_Copy.kr()",
        "PV_BinScramble.kr()",
        "PV_MagFreeze.kr()",
        "PV_MagMul.kr()",
        "IFFT.ar()",
        "Out.ar()",
    )
    assert str(py_synthdef_02) == normalize(
        """
        synthdef:
            name: PVCopyTest
            ugens:
            -   PinkNoise.ar: null
            -   MaxLocalBufs.ir:
                    maximum: 2.0
            -   LocalBuf.ir/0:
                    channel_count: 1.0
                    frame_count: 2048.0
            -   FFT.kr:
                    buffer_id: LocalBuf.ir/0[0]
                    source: PinkNoise.ar[0]
                    hop: 0.5
                    window_type: 0.0
                    active: 1.0
                    window_size: 0.0
            -   BufFrames.ir:
                    buffer_id: LocalBuf.ir/0[0]
            -   LocalBuf.ir/1:
                    channel_count: 1.0
                    frame_count: BufFrames.ir[0]
            -   PV_Copy.kr:
                    pv_chain_a: FFT.kr[0]
                    pv_chain_b: LocalBuf.ir/1[0]
            -   PV_BinScramble.kr:
                    pv_chain: PV_Copy.kr[0]
                    wipe: 0.0
                    width: 0.2
                    trigger: 0.0
            -   PV_MagFreeze.kr:
                    pv_chain: FFT.kr[0]
                    freeze: 0.0
            -   PV_MagMul.kr:
                    pv_chain_a: PV_BinScramble.kr[0]
                    pv_chain_b: PV_MagFreeze.kr[0]
            -   IFFT.ar:
                    pv_chain: PV_MagMul.kr[0]
                    window_type: 0.0
                    window_size: 0.0
            -   Out.ar:
                    bus: 0.0
                    source[0]: IFFT.ar[0]
        """
    )


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_02_supriya_vs_sclang(py_synthdef_02):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "PVCopyTest",
        r"""
        var source, pv_chain, pv_chain_a, pv_chain_b, ifft, out;
        source = PinkNoise.ar();
        pv_chain = FFT(LocalBuf(2048), source);
        pv_chain_a = PV_BinScramble(pv_chain);
        pv_chain_b = PV_MagFreeze(pv_chain);
        pv_chain = PV_MagMul(pv_chain_a, pv_chain_b);
        ifft = IFFT.ar(pv_chain);
        out = Out.ar(0, ifft);
        """,
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())
    py_compiled_synthdef = py_synthdef_02.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef
    sc_synthdef = supriya.synthdefs.SynthDefDecompiler.decompile_synthdef(
        sc_compiled_synthdef
    )
    assert tuple(repr(_) for _ in sc_synthdef.ugens) == (
        "PinkNoise.ar()",
        "MaxLocalBufs.ir()",
        "LocalBuf.ir()",
        "FFT.kr()",
        "BufFrames.ir()",
        "LocalBuf.ir()",
        "PV_Copy.kr()",
        "PV_BinScramble.kr()",
        "PV_MagFreeze.kr()",
        "PV_MagMul.kr()",
        "IFFT.ar()",
        "Out.ar()",
    )
    assert tuple(repr(_) for _ in sc_synthdef.ugens) == tuple(
        repr(_) for _ in py_synthdef_02.ugens
    )


def test_02_supriya_vs_bytes(py_synthdef_02):
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_02.compile()
    assert py_compiled_synthdef == test_compiled_synthdef
