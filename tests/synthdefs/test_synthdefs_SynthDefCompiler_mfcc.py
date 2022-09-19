# flake8: noqa
import platform

import pytest
from uqbar.strings import normalize

from supriya import SynthDefBuilder
from supriya.synthdefs import SuperColliderSynthDef, SynthDefDecompiler
from supriya.ugens import FFT, MFCC, In, Out


@pytest.fixture
def py_synthdef_mfcc():
    with SynthDefBuilder() as builder:
        source = In.ar(bus=0)
        pv_chain = FFT.kr(source=source)
        mfcc = MFCC.kr(pv_chain=pv_chain)
        Out.kr(bus=0, source=mfcc)
    return builder.build("MFCCTest")


@pytest.fixture
def sc_synthdef_mfcc():
    return SuperColliderSynthDef(
        "MFCCTest",
        r"""
        var in, fft, array;
        in = In.ar(0);
        fft = FFT(LocalBuf(2048), in);
        array = MFCC.kr(fft);
        Out.kr(0, array);
        """,
    )


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_ugens(py_synthdef_mfcc, sc_synthdef_mfcc):
    py_ugens = tuple(repr(_) for _ in py_synthdef_mfcc.ugens)
    assert py_ugens == (
        "In.ar()",
        "MaxLocalBufs.ir()",
        "LocalBuf.ir()",
        "FFT.kr()",
        "MFCC.kr()",
        "Out.kr()",
    )
    sc_compiled_synthdef = bytes(sc_synthdef_mfcc.compile())
    sc_synthdef = SynthDefDecompiler.decompile_synthdef(sc_compiled_synthdef)
    sc_ugens = tuple(repr(_) for _ in sc_synthdef.ugens)
    assert py_ugens == sc_ugens


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_format(py_synthdef_mfcc, sc_synthdef_mfcc):
    py_format = str(py_synthdef_mfcc)
    assert py_format == normalize(
        """
        synthdef:
            name: MFCCTest
            ugens:
            -   In.ar:
                    bus: 0.0
            -   MaxLocalBufs.ir:
                    maximum: 1.0
            -   LocalBuf.ir:
                    channel_count: 1.0
                    frame_count: 2048.0
            -   FFT.kr:
                    buffer_id: LocalBuf.ir[0]
                    source: In.ar[0]
                    hop: 0.5
                    window_type: 0.0
                    active: 1.0
                    window_size: 0.0
            -   MFCC.kr:
                    pv_chain: FFT.kr[0]
                    coeff_count: 13.0
            -   Out.kr:
                    bus: 0.0
                    source[0]: MFCC.kr[0]
                    source[1]: MFCC.kr[1]
                    source[2]: MFCC.kr[2]
                    source[3]: MFCC.kr[3]
                    source[4]: MFCC.kr[4]
                    source[5]: MFCC.kr[5]
                    source[6]: MFCC.kr[6]
                    source[7]: MFCC.kr[7]
                    source[8]: MFCC.kr[8]
                    source[9]: MFCC.kr[9]
                    source[10]: MFCC.kr[10]
                    source[11]: MFCC.kr[11]
                    source[12]: MFCC.kr[12]
        """
    )
    sc_compiled_synthdef = bytes(sc_synthdef_mfcc.compile())
    sc_synthdef = SynthDefDecompiler.decompile_synthdef(sc_compiled_synthdef)
    sc_format = str(sc_synthdef)
    assert py_format == sc_format


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_py_compile(py_synthdef_mfcc, sc_synthdef_mfcc):
    py_compiled_synthdef = py_synthdef_mfcc.compile()
    # fmt: off
    assert py_compiled_synthdef == (
        b"SCgf"
        b"\x00\x00\x00\x02"
        b"\x00\x01"
            b"\x08MFCCTest"
                b"\x00\x00\x00\x05"
                    b"\x00\x00\x00\x00"
                    b"?\x80\x00\x00"
                    b"E\x00\x00\x00"
                    b"?\x00\x00\x00"
                    b"AP\x00\x00"
                b"\x00\x00\x00\x00"
                b"\x00\x00\x00\x00"
                b"\x00\x00\x00\x06"
                    b"\x02In"
                        b"\x02"
                        b"\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02"
                    b"\x0cMaxLocalBufs"
                        b"\x00"
                        b"\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00"
                    b"\x08LocalBuf"
                        b"\x00"
                        b"\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00"
                    b"\x03FFT"
                        b"\x01"
                        b"\x00\x00\x00\x06\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\x01"
                    b"\x04MFCC"
                        b"\x01"
                        b"\x00\x00\x00\x02"
                        b"\x00\x00\x00\r"
                        b"\x00\x00"
                            b"\x00\x00\x00\x03"
                            b"\x00\x00\x00\x00"
                            b"\xff\xff\xff\xff"
                            b"\x00\x00\x00\x04"
                            b"\x01\x01\x01\x01"
                            b"\x01\x01\x01\x01"
                            b"\x01\x01\x01\x01"
                            b"\x01"
                    b"\x03Out"
                        b"\x01"
                        b"\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x04\x00\x00\x00\x06\x00\x00\x00\x04\x00\x00\x00\x07\x00\x00\x00\x04\x00\x00\x00\x08\x00\x00\x00\x04\x00\x00\x00\t\x00\x00\x00\x04\x00\x00\x00\n\x00\x00\x00\x04\x00\x00\x00\x0b\x00\x00\x00\x04\x00\x00\x00\x0c"
            b"\x00\x00"
    )
    # fmt: on
    sc_compiled_synthdef = bytes(sc_synthdef_mfcc.compile())
    assert sc_compiled_synthdef == py_compiled_synthdef
