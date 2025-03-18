# flake8: noqa
import os
import platform

import pytest

from supriya.ugens import Out, SinOsc, SuperColliderSynthDef, SynthDef, SynthDefBuilder


@pytest.fixture
def py_synthdef() -> SynthDef:
    with SynthDefBuilder() as builder:
        sine_a = SinOsc.ar(frequency=420)
        sine_b = SinOsc.ar(frequency=440)  # noqa
        sine_c = SinOsc.ar(frequency=460)
        sine_d = SinOsc.ar(frequency=sine_c)  # noqa
        Out.ar(bus=0, source=sine_a)
    py_synthdef = builder.build("optimized")
    return py_synthdef


def test_optimization_01_supriya_vs_bytes(py_synthdef: SynthDef) -> None:
    # fmt: off
    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\toptimized'
                b'\x00\x00\x00\x02'
                    b'C\xd2\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x02'
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
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                b'\x00\x00'
    )
    # fmt: on
    py_compiled_synthdef = py_synthdef.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_optimization_01_supriya_vs_sclang(py_synthdef: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "optimized",
        r"""
        var sine_a, sine_b, sine_c, sine_d;
        sine_a = SinOsc.ar(420);
        sine_b = SinOsc.ar(440);
        sine_c = SinOsc.ar(460);
        sine_d = SinOsc.ar(sine_c);
        Out.ar(0, sine_a);
        """,
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())
    py_compiled_synthdef = py_synthdef.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef
