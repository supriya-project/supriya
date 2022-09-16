# flake8: noqa
import platform

import pytest

import supriya.synthdefs
import supriya.ugens


@pytest.fixture
def py_synthdef():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        source = supriya.ugens.PinkNoise.ar()
        azimuth = supriya.ugens.LFNoise2.kr(frequency=0.25)
        w, x, y = supriya.ugens.PanB2.ar(source=source, azimuth=azimuth)
        source = supriya.ugens.DecodeB2.ar(
            channel_count=4, w=w, x=x, y=y, orientation=0.5
        )
        supriya.ugens.Out.ar(bus=0, source=source)
    py_synthdef = builder.build("ambisonics")
    return py_synthdef


def test_SynthDefCompiler_ambisonics_supriya_vs_bytes(py_synthdef):
    # fmt: off
    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\nambisonics'
                b'\x00\x00\x00\x04'
                    b'>\x80\x00\x00'
                    b'?\x80\x00\x00'
                    b'?\x00\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x05'
                    b'\tPinkNoise'
                        b'\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x02'
                    b'\x08LFNoise2'
                        b'\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x01'
                    b'\x05PanB2'
                        b'\x02'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\x02'
                            b'\x02'
                            b'\x02'
                    b'\x08DecodeB2'
                        b'\x02'
                        b'\x00\x00\x00\x04'
                        b'\x00\x00\x00\x04'
                        b'\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x02'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x02'
                            b'\x02'
                            b'\x02'
                            b'\x02'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x05'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x03'
                b'\x00\x00'
    )
    # fmt: on
    py_compiled_synthdef = py_synthdef.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_SynthDefCompiler_ambisonics_supriya_vs_sclang(py_synthdef):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "ambisonics",
        r"""
        var source, azimuth, w, x, y;
        source = PinkNoise.ar();
        azimuth = LFNoise2.kr(0.25);
        #w, x, y = PanB2.ar(source, azimuth, 1);
        source = DecodeB2.ar(4, w, x, y, 0.5);
        Out.ar(0, source);
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef.compile()
    assert sc_compiled_synthdef == py_compiled_synthdef
