# flake8: noqa
import os
import platform

import pytest

from supriya.ugens import (
    Demand,
    Dseries,
    Impulse,
    Out,
    SinOsc,
    SuperColliderSynthDef,
    SynthDef,
    SynthDefBuilder,
)


@pytest.fixture
def py_synthdef() -> SynthDef:
    with SynthDefBuilder() as builder:
        series = Dseries.dr(length=float("inf"), start=0, step=1)
        trigger = Impulse.kr(frequency=10)
        frequency = Demand.kr(trigger=trigger, source=series)
        Out.ar(bus=0, source=SinOsc.ar(frequency=frequency))
    py_synthdef = builder.build("foo")
    return py_synthdef


def test_demand_supriya_vs_bytes(py_synthdef: SynthDef) -> None:
    # fmt: off
    test_compiled_synthdef = bytes(
         b'SCgf'
         b'\x00\x00\x00\x02'
         b'\x00\x01'
             b'\x03foo'
                 b'\x00\x00\x00\x04'
                     b'\x7f\x80\x00\x00'
                     b'\x00\x00\x00\x00'
                     b'?\x80\x00\x00'
                     b'A \x00\x00'
                 b'\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00'
                 b'\x00\x00\x00\x05'
                     b'\x07Dseries'
                        b'\x03'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x02'
                            b'\x03'
                     b'\x07Impulse'
                        b'\x01'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x03'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x01'
                     b'\x06Demand'
                        b'\x01'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x01'
                     b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x02'
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
                            b'\x00\x00\x00\x03'
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
def test_demand_supriya_vs_sclang(py_synthdef: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "foo",
        """
        var series, trigger, frequency;
        series = Dseries(0, 1, inf);
        trigger = Impulse.kr(frequency=10);
        frequency = Demand.kr(trigger, 0, series);
        Out.ar(0, SinOsc.ar(frequency));
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef
