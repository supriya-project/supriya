import os
import platform

import pytest
from uqbar.strings import normalize

from supriya.assets.synthdefs import system_link_audio_1, system_link_audio_2
from supriya.ugens import SuperColliderSynthDef, decompile_synthdef


def test_system_link_audio_1_supriya() -> None:
    assert normalize(str(system_link_audio_1)) == normalize(
        """
        synthdef:
            name: system_link_audio_1
            ugens:
            -   Control.kr:
                    done_action: 2.0
                    fade_time: 0.02
                    gate: 1.0
                    in_: 16.0
                    out: 0.0
            -   BinaryOpUGen(LESS_THAN_OR_EQUAL).kr:
                    left: Control.kr[1:fade_time]
                    right: 0.0
            -   EnvGen.kr:
                    gate: Control.kr[2:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: Control.kr[1:fade_time]
                    done_action: Control.kr[0:done_action]
                    envelope[0]: BinaryOpUGen(LESS_THAN_OR_EQUAL).kr[0]
                    envelope[1]: 2.0
                    envelope[2]: 1.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 1.0
                    envelope[6]: 3.0
                    envelope[7]: 0.0
                    envelope[8]: 0.0
                    envelope[9]: 1.0
                    envelope[10]: 3.0
                    envelope[11]: 0.0
            -   InFeedback.ar:
                    bus: Control.kr[3:in_]
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: InFeedback.ar[0]
                    right: EnvGen.kr[0]
            -   Out.ar:
                    bus: Control.kr[4:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """
    )


def test_system_link_audio_1_bytes() -> None:
    py_compiled = system_link_audio_1.compile()
    assert py_compiled == (
        b"SCgf\x00\x00\x00\x02\x00\x01\x13system_link_audio_1\x00\x00\x00\x05\x00\x00"
        b"\x00\x00?\x80\x00\x00@\x00\x00\x00\xc2\xc6\x00\x00@@\x00\x00\x00\x00"
        b"\x00\x05@\x00\x00\x00<\xa3\xd7\n?\x80\x00\x00A\x80\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x05\x0bdone_action\x00\x00\x00\x00\tfade_time"
        b"\x00\x00\x00\x01\x04gate\x00\x00\x00\x02\x03in_\x00\x00\x00\x03\x03ou"
        b"t\x00\x00\x00\x04\x00\x00\x00\x06\x07Control\x01\x00\x00\x00\x00\x00\x00"
        b"\x00\x05\x00\x00\x01\x01\x01\x01\x01\x0cBinaryOpUGen\x01\x00\x00\x00\x02\x00"
        b"\x00\x00\x01\x00\n\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff"
        b"\xff\x00\x00\x00\x00\x01\x06EnvGen\x01\x00\x00\x00\x11\x00\x00"
        b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xff\xff\xff"
        b"\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
        b"\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x02\xff\xff\xff\xff"
        b"\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff"
        b"\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff"
        b"\x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff"
        b"\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff"
        b"\x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x00\x01\nInFeedback"
        b"\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x03\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02"
        b"\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x02\x03Ou"
        b"t\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00"
    )


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_system_link_audio_1_sclang() -> None:
    sc_compiled = SuperColliderSynthDef(
        "system_link_audio_1",
        r"""
        | out=0, in=16, vol=1, level=1, lag=0.05, doneAction=2 |
        var env = EnvGate(i_level: 0, doneAction:doneAction, curve:'sin')
        * Lag.kr(vol * level, lag);
        Out.ar(out, InFeedback.ar(in, 1) * env)
        """,
        r"[\kr, \kr, \kr, \kr, \kr, \ir]",
    ).compile()
    sc_synthdef = decompile_synthdef(sc_compiled)
    assert normalize(str(sc_synthdef)) == normalize(
        """
        synthdef:
            name: system_link_audio_1
            ugens:
            -   Control.ir:
                    doneAction: 2.0
            -   Control.kr:
                    out: 0.0
                    in: 16.0
                    vol: 1.0
                    level: 1.0
                    lag: 0.05000000074505806
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Control.kr[2:vol]
                    right: Control.kr[3:level]
            -   Lag.kr:
                    source: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    lag_time: Control.kr[4:lag]
            -   InFeedback.ar:
                    bus: Control.kr[1:in]
            -   Control.kr:
                    gate: 1.0
            -   Control.kr:
                    fadeTime: 0.019999999552965164
            -   EnvGen.kr:
                    gate: Control.kr[0:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: Control.kr[0:fadeTime]
                    done_action: Control.ir[0:doneAction]
                    envelope[0]: 0.0
                    envelope[1]: 2.0
                    envelope[2]: 1.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 1.0
                    envelope[6]: 3.0
                    envelope[7]: 0.0
                    envelope[8]: 0.0
                    envelope[9]: 1.0
                    envelope[10]: 3.0
                    envelope[11]: 0.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: EnvGen.kr[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: InFeedback.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   Out.ar:
                    bus: Control.kr[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """
    )


def test_system_link_audio_2_supriya() -> None:
    assert normalize(str(system_link_audio_2)) == normalize(
        """
        synthdef:
            name: system_link_audio_2
            ugens:
            -   Control.kr:
                    done_action: 2.0
                    fade_time: 0.02
                    gate: 1.0
                    in_: 16.0
                    out: 0.0
            -   BinaryOpUGen(LESS_THAN_OR_EQUAL).kr:
                    left: Control.kr[1:fade_time]
                    right: 0.0
            -   EnvGen.kr:
                    gate: Control.kr[2:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: Control.kr[1:fade_time]
                    done_action: Control.kr[0:done_action]
                    envelope[0]: BinaryOpUGen(LESS_THAN_OR_EQUAL).kr[0]
                    envelope[1]: 2.0
                    envelope[2]: 1.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 1.0
                    envelope[6]: 3.0
                    envelope[7]: 0.0
                    envelope[8]: 0.0
                    envelope[9]: 1.0
                    envelope[10]: 3.0
                    envelope[11]: 0.0
            -   InFeedback.ar:
                    bus: Control.kr[3:in_]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: InFeedback.ar[0]
                    right: EnvGen.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: InFeedback.ar[1]
                    right: EnvGen.kr[0]
            -   Out.ar:
                    bus: Control.kr[4:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
        """
    )


def test_system_link_audio_2_bytes() -> None:
    py_compiled = system_link_audio_2.compile()
    assert py_compiled == (
        b"SCgf\x00\x00\x00\x02\x00\x01\x13system_link_audio_2\x00\x00\x00\x05\x00\x00"
        b"\x00\x00?\x80\x00\x00@\x00\x00\x00\xc2\xc6\x00\x00@@\x00\x00\x00\x00"
        b"\x00\x05@\x00\x00\x00<\xa3\xd7\n?\x80\x00\x00A\x80\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x05\x0bdone_action\x00\x00\x00\x00\tfade_time"
        b"\x00\x00\x00\x01\x04gate\x00\x00\x00\x02\x03in_\x00\x00\x00\x03\x03ou"
        b"t\x00\x00\x00\x04\x00\x00\x00\x07\x07Control\x01\x00\x00\x00\x00\x00\x00"
        b"\x00\x05\x00\x00\x01\x01\x01\x01\x01\x0cBinaryOpUGen\x01\x00\x00\x00\x02\x00"
        b"\x00\x00\x01\x00\n\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff"
        b"\xff\x00\x00\x00\x00\x01\x06EnvGen\x01\x00\x00\x00\x11\x00\x00"
        b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xff\xff\xff"
        b"\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
        b"\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x02\xff\xff\xff\xff"
        b"\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff"
        b"\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff"
        b"\x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff"
        b"\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff"
        b"\x00\x00\x00\x04\xff\xff\xff\xff\x00\x00\x00\x00\x01\nInFeedback"
        b"\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x03\x02\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00"
        b"\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00"
        b"\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00"
        b"\x00\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x02\x03Out\x02"
        b"\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00"
        b"\x00\x00\x00\x00"
    )


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_system_link_audio_2_sclang() -> None:
    sc_compiled = SuperColliderSynthDef(
        "system_link_audio_2",
        r"""
        | out=0, in=16, vol=1, level=1, lag=0.05, doneAction=2 |
        var env = EnvGate(i_level: 0, doneAction:doneAction, curve:'sin')
        * Lag.kr(vol * level, lag);
        Out.ar(out, InFeedback.ar(in, 2) * env)
        """,
        r"[\kr, \kr, \kr, \kr, \kr, \ir]",
    ).compile()
    sc_synthdef = decompile_synthdef(sc_compiled)
    assert normalize(str(sc_synthdef)) == normalize(
        """
        synthdef:
            name: system_link_audio_2
            ugens:
            -   Control.ir:
                    doneAction: 2.0
            -   Control.kr:
                    out: 0.0
                    in: 16.0
                    vol: 1.0
                    level: 1.0
                    lag: 0.05000000074505806
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Control.kr[2:vol]
                    right: Control.kr[3:level]
            -   Lag.kr:
                    source: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    lag_time: Control.kr[4:lag]
            -   InFeedback.ar:
                    bus: Control.kr[1:in]
            -   Control.kr:
                    gate: 1.0
            -   Control.kr:
                    fadeTime: 0.019999999552965164
            -   EnvGen.kr:
                    gate: Control.kr[0:gate]
                    level_scale: 1.0
                    level_bias: 0.0
                    time_scale: Control.kr[0:fadeTime]
                    done_action: Control.ir[0:doneAction]
                    envelope[0]: 0.0
                    envelope[1]: 2.0
                    envelope[2]: 1.0
                    envelope[3]: -99.0
                    envelope[4]: 1.0
                    envelope[5]: 1.0
                    envelope[6]: 3.0
                    envelope[7]: 0.0
                    envelope[8]: 0.0
                    envelope[9]: 1.0
                    envelope[10]: 3.0
                    envelope[11]: 0.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: EnvGen.kr[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: InFeedback.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: InFeedback.ar[1]
                    right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   Out.ar:
                    bus: Control.kr[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
        """
    )
