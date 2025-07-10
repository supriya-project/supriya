import pytest
from uqbar.strings import normalize

from supriya import SynthDef
from supriya.ugens.system import build_channel_strip_synthdef


@pytest.mark.parametrize(
    "synthdef, expected_str",
    [
        (
            build_channel_strip_synthdef(2),
            """
            synthdef:
                name: supriya:channel-strip:2
                ugens:
                -   LagControl.kr:
                        active: 1.0
                        done_action: 2.0
                        gain: 0.0
                        gate: 1.0
                        out: 0.0
                        lags[0]: 0.0
                        lags[1]: 0.0
                        lags[2]: 0.05
                        lags[3]: 0.0
                        lags[4]: 0.0
                -   In.ar:
                        channel_count: 2
                        bus: LagControl.kr[4:out]
                -   Linen.kr/0:
                        gate: LagControl.kr[0:active]
                        attack_time: 0.05
                        sustain_level: 1.0
                        release_time: 0.05
                        done_action: 0.0
                -   Linen.kr/1:
                        gate: LagControl.kr[3:gate]
                        attack_time: 0.05
                        sustain_level: 1.0
                        release_time: 0.05
                        done_action: LagControl.kr[1:done_action]
                -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                        source: LagControl.kr[2:gain]
                -   BinaryOpUGen(MULTIPLICATION).ar/0:
                        left: In.ar[0]
                        right: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        right: Linen.kr/0[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/2:
                        left: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        right: Linen.kr/1[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/3:
                        left: In.ar[1]
                        right: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/4:
                        left: BinaryOpUGen(MULTIPLICATION).ar/3[0]
                        right: Linen.kr/0[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/5:
                        left: BinaryOpUGen(MULTIPLICATION).ar/4[0]
                        right: Linen.kr/1[0]
                -   ReplaceOut.ar:
                        bus: LagControl.kr[4:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/5[0]
            """,
        ),
    ],
)
def test_synthdefs(
    synthdef: SynthDef,
    expected_str: str,
) -> None:
    assert normalize(str(synthdef)) == normalize(expected_str)
