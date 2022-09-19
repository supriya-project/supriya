# flake8: noqa
import platform

import pytest

import supriya.synthdefs
import supriya.ugens


@pytest.fixture
def py_synthdef_01():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        sine_one = supriya.ugens.SinOsc.ar(frequency=420)
        sine_two = supriya.ugens.SinOsc.ar(frequency=440)
        sines = sine_one * sine_two
        supriya.ugens.Out.ar(bus=0, source=sines)
    py_synthdef = builder.build("foo")
    return py_synthdef


def test_SynthDefCompiler_basic_01_supriya_vs_bytes(py_synthdef_01):
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_01.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_SynthDefCompiler_basic_01_supriya_vs_sclang(py_synthdef_01):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "foo", "Out.ar(0, SinOsc.ar(freq: 420) * SinOsc.ar(freq: 440))"
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_01.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.fixture
def py_synthdef_02():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        sine = supriya.ugens.SinOsc.ar()
        sine = -sine
        supriya.ugens.Out.ar(bus=99, source=sine)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_SynthDefCompiler_basic_02_supriya_vs_bytes(py_synthdef_02):
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_02.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_SynthDefCompiler_basic_02_supriya_vs_sclang(py_synthdef_02):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "test", "Out.ar(99, SinOsc.ar(freq: 440).neg)"
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_02.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.fixture
def py_synthdef_03():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        inputs = supriya.ugens.In.ar(bus=8, channel_count=2)
        supriya.ugens.Out.ar(bus=0, source=inputs)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_SynthDefCompiler_basic_03_supriya_vs_bytes(py_synthdef_03):
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_03.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_SynthDefCompiler_basic_03_supriya_vs_sclang(py_synthdef_03):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "test",
        r"""
        Out.ar(0, In.ar(8, 2))
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_03.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.fixture
def py_synthdef_04():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        sin_osc = supriya.ugens.SinOsc.ar()
        supriya.ugens.FreeSelf.kr(trigger=sin_osc)
        supriya.ugens.Out.ar(bus=0, source=sin_osc)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_SynthDefCompiler_basic_04_supriya_vs_bytes(py_synthdef_04):
    """
    FreeSelf.
    """
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_04.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_SynthDefCompiler_basic_04_supriya_vs_sclang(py_synthdef_04):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "test",
        r"""
        Out.ar(0, FreeSelf.kr(SinOsc.ar()))
        """,
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())
    py_compiled_synthdef = py_synthdef_04.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_SynthDefCompiler_basic_05_supriya_vs_sclang():
    with supriya.synthdefs.SynthDefBuilder() as builder:
        source = supriya.ugens.In.ar(bus=8, channel_count=2)
        supriya.ugens.DetectSilence.ar(source=source)
        supriya.ugens.Out.ar(bus=0, source=source)
    py_synthdef = builder.build("DetectSilenceTest")
    py_compiled_synthdef = py_synthdef.compile()
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "DetectSilenceTest",
        r"""
        var source, detect_silence, out;
        source = In.ar(8, 2);
        detect_silence = DetectSilence.ar(source);
        out = Out.ar(0, source);
        """,
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())
    assert py_compiled_synthdef == sc_compiled_synthdef
