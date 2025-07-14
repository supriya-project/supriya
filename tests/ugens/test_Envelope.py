import pytest
from pytest_lazy_fixtures import lf
from uqbar.strings import normalize

from supriya.ugens import Envelope, EnvGen, Out, SynthDef, SynthDefBuilder


@pytest.fixture
def envelope_a() -> SynthDef:
    with SynthDefBuilder(out=0, decay=1) as builder:
        envelope = Envelope([0.11, 1, 0], [0, builder["decay"]], [-225])
        envgen = EnvGen.kr(envelope=envelope)
        Out.kr(bus=builder["out"], source=envgen)
    return builder.build(name="test-envelope-expansion")


@pytest.fixture
def envelope_b() -> SynthDef:
    with SynthDefBuilder(out=0, decay=[1, 2]) as builder:
        envelope = Envelope([0.11, 1, 0], [0, builder["decay"]], [-225])
        envgen = EnvGen.kr(envelope=envelope)
        Out.kr(bus=builder["out"], source=envgen)
    return builder.build(name="test-envelope-expansion")


@pytest.mark.parametrize(
    "synthdef, expected_str",
    [
        (
            lf("envelope_a"),
            """
            synthdef:
                name: test-envelope-expansion
                ugens:
                -   Control.kr:
                        decay: 1.0
                        out: 0.0
                -   EnvGen.kr:
                        gate: 1.0
                        level_scale: 1.0
                        level_bias: 0.0
                        time_scale: 1.0
                        done_action: 0.0
                        envelope[0]: 0.11
                        envelope[1]: 2.0
                        envelope[2]: -99.0
                        envelope[3]: -99.0
                        envelope[4]: 1.0
                        envelope[5]: 0.0
                        envelope[6]: 5.0
                        envelope[7]: -225.0
                        envelope[8]: 0.0
                        envelope[9]: Control.kr[0:decay]
                        envelope[10]: 5.0
                        envelope[11]: -225.0
                -   Out.kr:
                        bus: Control.kr[1:out]
                        source[0]: EnvGen.kr[0]
            """,
        ),
        (
            lf("envelope_b"),
            """
            synthdef:
                name: test-envelope-expansion
                ugens:
                -   Control.kr:
                        decay[0]: 1.0
                        decay[1]: 2.0
                        out: 0.0
                -   EnvGen.kr/0:
                        gate: 1.0
                        level_scale: 1.0
                        level_bias: 0.0
                        time_scale: 1.0
                        done_action: 0.0
                        envelope[0]: 0.11
                        envelope[1]: 2.0
                        envelope[2]: -99.0
                        envelope[3]: -99.0
                        envelope[4]: 1.0
                        envelope[5]: 0.0
                        envelope[6]: 5.0
                        envelope[7]: -225.0
                        envelope[8]: 0.0
                        envelope[9]: Control.kr[0:decay[0]]
                        envelope[10]: 5.0
                        envelope[11]: -225.0
                -   EnvGen.kr/1:
                        gate: 1.0
                        level_scale: 1.0
                        level_bias: 0.0
                        time_scale: 1.0
                        done_action: 0.0
                        envelope[0]: 0.11
                        envelope[1]: 2.0
                        envelope[2]: -99.0
                        envelope[3]: -99.0
                        envelope[4]: 1.0
                        envelope[5]: 0.0
                        envelope[6]: 5.0
                        envelope[7]: -225.0
                        envelope[8]: 0.0
                        envelope[9]: Control.kr[1:decay[1]]
                        envelope[10]: 5.0
                        envelope[11]: -225.0
                -   Out.kr:
                        bus: Control.kr[2:out]
                        source[0]: EnvGen.kr/0[0]
                        source[1]: EnvGen.kr/1[0]
            """,
        ),
    ],
)
def test_Envelope_serialize(synthdef: SynthDef, expected_str: str):
    """
    Envelopes shouldn't expand trivial UGenOperable inputs.
    """
    assert str(synthdef) == normalize(expected_str)
