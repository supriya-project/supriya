# flake8: noqa
import os
import platform

import pytest
from uqbar.strings import normalize

from supriya.enums import ParameterRate
from supriya.ugens import (
    Decay2,
    DelayC,
    In,
    Mix,
    Out,
    Parameter,
    SinOsc,
    SuperColliderSynthDef,
    SynthDef,
    SynthDefBuilder,
)


@pytest.fixture
def py_synthdef_01() -> SynthDef:
    with SynthDefBuilder(freq=440) as builder:
        sine = SinOsc.ar(frequency=builder["freq"])
        Out.ar(bus=0, source=sine)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_parameters_01_parameters(py_synthdef_01: SynthDef) -> None:
    assert py_synthdef_01.indexed_parameters == [
        (
            0,
            Parameter(name="freq", rate=ParameterRate.CONTROL, value=440.0),
        ),
    ]


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_parameters_01_supriya_vs_sclang(py_synthdef_01: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "test",
        r"""
        | freq = 440 |
        Out.ar(0, SinOsc.ar(freq: freq))
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_01.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


def test_parameters_01_supriya_vs_bytes(py_synthdef_01: SynthDef) -> None:
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_01.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.fixture
def py_synthdef_02() -> SynthDef:
    with SynthDefBuilder(freq=1200, out=23) as builder:
        sine = SinOsc.ar(frequency=builder["freq"])
        Out.ar(bus=builder["out"], source=sine)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_parameters_02_parameters(py_synthdef_02: SynthDef) -> None:
    assert py_synthdef_02.indexed_parameters == [
        (
            0,
            Parameter(name="freq", rate=ParameterRate.CONTROL, value=1200.0),
        ),
        (
            1,
            Parameter(name="out", rate=ParameterRate.CONTROL, value=23.0),
        ),
    ]


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_parameters_02_supriya_vs_sclang(py_synthdef_02: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "test",
        r"""
        arg freq=1200, out=23;
        Out.ar(out, SinOsc.ar(freq: freq));
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_02.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


def test_parameters_02_supriya_vs_bytes(py_synthdef_02: SynthDef) -> None:
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_02.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.fixture
def py_synthdef_03() -> SynthDef:
    builder = SynthDefBuilder(damping=0.1, delay_time=1.0, room_size=0.9)
    with builder:
        microphone = In.ar(bus=0)
        delay = DelayC.ar(
            source=microphone, maximum_delay_time=5.0, delay_time=builder["delay_time"]
        )
        Out.ar(bus=0, source=delay)
    py_synthdef = builder.build("test")
    return py_synthdef


def test_parameters_03_parameters(py_synthdef_03: SynthDef) -> None:
    """
    Multiple parameters, including unused parameters.
    """
    assert py_synthdef_03.indexed_parameters == [
        (
            0,
            Parameter(name="damping", rate=ParameterRate.CONTROL, value=0.1),
        ),
        (
            1,
            Parameter(name="delay_time", rate=ParameterRate.CONTROL, value=1.0),
        ),
        (
            2,
            Parameter(name="room_size", rate=ParameterRate.CONTROL, value=0.9),
        ),
    ]


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_parameters_03_supriya_vs_sclang(py_synthdef_03: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "test",
        r"""
        | damping=0.1, delay_time=1.0, room_size=0.9 |
        Out.ar(0, DelayC.ar(In.ar(0), 5.0, delay_time))
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    py_compiled_synthdef = py_synthdef_03.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


def test_parameters_03_supriya_vs_bytes(py_synthdef_03: SynthDef) -> None:
    # fmt: off
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
    # fmt: on
    py_compiled_synthdef = py_synthdef_03.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.fixture
def py_synthdef_04() -> SynthDef:
    builder = SynthDefBuilder(
        a_phase=0.0, freq=440, i_decay_time=1.0, t_trig_a=0, t_trig_b=0
    )
    with builder:
        decay = Decay2.kr(
            source=(builder["t_trig_a"], builder["t_trig_b"]),
            attack_time=0.005,
            decay_time=builder["i_decay_time"],
        )
        sin_osc = SinOsc.ar(frequency=builder["freq"], phase=builder["a_phase"])
        enveloped_sin_osc = sin_osc * decay
        Out.ar(bus=0, source=enveloped_sin_osc)
    py_synthdef = builder.build("trigTest")
    return py_synthdef


@pytest.fixture
def py_synthdef_05() -> SynthDef:
    builder = SynthDefBuilder(amp=0.1, freqs=[300, 400])
    with builder:
        sines = SinOsc.ar(frequency=builder["freqs"])
        sines = Mix.new(sines)
        sines = sines * builder["amp"]
        Out.ar(bus=0, source=sines)
    py_synthdef = builder.build("arrayarg")
    return py_synthdef


def test_parameters_05_parameters(py_synthdef_05: SynthDef) -> None:
    """
    Literal array arguments.
    """
    assert py_synthdef_05.indexed_parameters == [
        (
            0,
            Parameter(name="amp", rate=ParameterRate.CONTROL, value=0.1),
        ),
        (
            1,
            Parameter(name="freqs", rate=ParameterRate.CONTROL, value=(300.0, 400.0)),
        ),
    ]


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_parameters_05_supriya_vs_sclang(py_synthdef_05: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "arrayarg",
        r"""
        |
            amp = 0.1,
            freqs = #[300, 400]
        |
        var sines;
        sines = SinOsc.ar(freqs).sum;
        Out.ar(0, sines * amp);
        """,
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())
    py_compiled_synthdef = py_synthdef_05.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


def test_parameters_05_supriya_vs_bytes(py_synthdef_05: SynthDef) -> None:
    # fmt: off
    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x08arrayarg'
                b'\x00\x00\x00\x01'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x03'
                    b'=\xcc\xcc\xcd'
                    b'C\x96\x00\x00'
                    b'C\xc8\x00\x00'
                b'\x00\x00\x00\x02'
                    b'\x03amp'
                        b'\x00\x00\x00\x00'
                    b'\x05freqs'
                        b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x06'
                    b'\x07Control'
                        b'\x01'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00'
                            b'\x01'
                            b'\x01'
                            b'\x01'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x01'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x02'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x0cBinaryOpUGen'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x0cBinaryOpUGen'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x02'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x04'
                                b'\x00\x00\x00\x00'
                b'\x00\x00'
    )
    # fmt: on
    py_compiled_synthdef = py_synthdef_05.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


@pytest.fixture
def py_synthdef_06() -> SynthDef:
    builder = SynthDefBuilder(amp=0.1, freqs=Parameter(lag=0.5, value=[300, 400]))
    with builder:
        sines = SinOsc.ar(frequency=builder["freqs"])
        sines = Mix.new(sines)
        sines = sines * builder["amp"]
        Out.ar(bus=0, source=sines)
    py_synthdef = builder.build("arrayarg")
    return py_synthdef


def test_parameters_06_parameters(py_synthdef_06: SynthDef) -> None:
    """
    Literal array arguments.
    """
    assert py_synthdef_06.indexed_parameters == [
        (
            0,
            Parameter(name="amp", rate=ParameterRate.CONTROL, value=0.1),
        ),
        (
            1,
            Parameter(
                lag=0.5,
                name="freqs",
                rate=ParameterRate.CONTROL,
                value=(300.0, 400.0),
            ),
        ),
    ]


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_parameters_06_supriya_vs_sclang(py_synthdef_06: SynthDef) -> None:
    sc_synthdef = SuperColliderSynthDef(
        "arrayarg",
        r"""
        |
            amp = 0.1,
            freqs = #[300, 400]
        |
        var sines;
        sines = SinOsc.ar(freqs).sum;
        Out.ar(0, sines * amp);
        """,
        "[0, 0.5]",
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())
    py_compiled_synthdef = py_synthdef_06.compile()
    assert py_compiled_synthdef == sc_compiled_synthdef


def test_parameters_06_supriya_vs_bytes(py_synthdef_06: SynthDef) -> None:
    # fmt: off
    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x08arrayarg'
                b'\x00\x00\x00\x02'
                    b'\x00\x00\x00\x00'
                    b'?\x00\x00\x00'
                b'\x00\x00\x00\x03'
                    b'=\xcc\xcc\xcd'
                    b'C\x96\x00\x00'
                    b'C\xc8\x00\x00'
                b'\x00\x00\x00\x02'
                    b'\x03amp'
                        b'\x00\x00\x00\x00'
                    b'\x05freqs'
                        b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x06'
                    b'\nLagControl'
                        b'\x01'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\x01'
                            b'\x01'
                            b'\x01'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x01'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x02'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x0cBinaryOpUGen'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x0cBinaryOpUGen'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x02'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x04'
                                b'\x00\x00\x00\x00'
                b'\x00\x00'
    )
    # fmt: on
    py_compiled_synthdef = py_synthdef_06.compile()
    assert py_compiled_synthdef == test_compiled_synthdef


def test_parameters_07() -> None:
    builder = SynthDefBuilder(amplitude=0, bus=0, frequency=440)
    with builder:
        sine = SinOsc.ar(frequency=builder["frequency"])
        source = sine * builder["amplitude"]
        Out.ar(bus=builder["bus"], source=source)
    synthdef = builder.build(name="simple_sine")
    assert normalize(str(synthdef)) == normalize(
        """
        synthdef:
            name: simple_sine
            ugens:
            -   Control.kr:
                    amplitude: 0.0
                    bus: 0.0
                    frequency: 440.0
            -   SinOsc.ar:
                    frequency: Control.kr[2:frequency]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: SinOsc.ar[0]
                    right: Control.kr[0:amplitude]
            -   Out.ar:
                    bus: Control.kr[1:bus]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """
    )


def test_building_is_idempotent() -> None:
    builder = SynthDefBuilder(amplitude=0, bus=0, frequency=440)
    with builder as builder:
        sine = SinOsc.ar(frequency=builder["frequency"])
        source = sine * builder["amplitude"]
        Out.ar(bus=builder["bus"], source=source)
    synthdef_a = builder.build()
    synthdef_b = builder.build()
    synthdef_c = builder.build()
    assert normalize(str(synthdef_a)) == normalize(
        """
        synthdef:
            name: 937772273a43d21bcd7b9f096f42648a
            ugens:
            -   Control.kr:
                    amplitude: 0.0
                    bus: 0.0
                    frequency: 440.0
            -   SinOsc.ar:
                    frequency: Control.kr[2:frequency]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: SinOsc.ar[0]
                    right: Control.kr[0:amplitude]
            -   Out.ar:
                    bus: Control.kr[1:bus]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """
    )
    assert str(synthdef_a) == str(synthdef_b)
    assert str(synthdef_b) == str(synthdef_c)
