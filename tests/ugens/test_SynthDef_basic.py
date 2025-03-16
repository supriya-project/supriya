# flake8: noqa
import os
import platform

import pytest

from supriya.ugens import (
    DetectSilence,
    FreeSelf,
    In,
    Out,
    SinOsc,
    SuperColliderSynthDef,
    SynthDef,
    SynthDefBuilder,
)


@pytest.fixture
def py_synthdef_01() -> SynthDef:
    with SynthDefBuilder() as builder:
        sine_one = SinOsc.ar(frequency=420)
        sine_two = SinOsc.ar(frequency=440)
        sines = sine_one * sine_two
        Out.ar(bus=0, source=sines)
    py_synthdef = builder.build("foo")
    return py_synthdef


def test_basic_01_supriya_vs_bytes(py_synthdef_01: SynthDef) -> None:
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
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_basic_01_supriya_vs_sclang(py_synthdef_01: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "foo", "Out.ar(0, SinOsc.ar(freq: 420) * SinOsc.ar(freq: 440))"
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_01.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.fixture
def py_synthdef_02() -> SynthDef:
    with SynthDefBuilder() as builder:
        sine = SinOsc.ar()
        sine = -sine
        Out.ar(bus=99, source=sine)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_basic_02_supriya_vs_bytes(py_synthdef_02: SynthDef) -> None:
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
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_basic_02_supriya_vs_sclang(py_synthdef_02: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef("test", "Out.ar(99, SinOsc.ar(freq: 440).neg)")
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_02.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.fixture
def py_synthdef_03() -> SynthDef:
    with SynthDefBuilder() as builder:
        inputs = In.ar(bus=8, channel_count=2)
        Out.ar(bus=0, source=inputs)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_basic_03_supriya_vs_bytes(py_synthdef_03: SynthDef) -> None:
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
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_basic_03_supriya_vs_sclang(py_synthdef_03: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "test",
        r"""
        Out.ar(0, In.ar(8, 2))
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_03.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.fixture
def py_synthdef_04() -> SynthDef:
    with SynthDefBuilder() as builder:
        sin_osc = SinOsc.ar()
        FreeSelf.kr(trigger=sin_osc)
        Out.ar(bus=0, source=sin_osc)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_basic_04_supriya_vs_bytes(py_synthdef_04: SynthDef) -> None:
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
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_basic_04_supriya_vs_sclang(py_synthdef_04: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "test",
        r"""
        Out.ar(0, FreeSelf.kr(SinOsc.ar()))
        """,
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())
    py_compiled_synthdef = py_synthdef_04.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_basic_05_supriya_vs_sclang() -> None:
    with SynthDefBuilder() as builder:
        source = In.ar(bus=8, channel_count=2)
        DetectSilence.ar(source=source)
        Out.ar(bus=0, source=source)
    py_synthdef = builder.build("DetectSilenceTest")
    py_compiled_synthdef = py_synthdef.compile()
    sc_synthdef = SuperColliderSynthDef(
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
