import logging

import pytest

from supriya.enums import ParameterRate
from supriya.ugens import Out, Parameter, SinOsc, SynthDef, SynthDefBuilder


@pytest.fixture(autouse=True)
def capture_logs(caplog):
    caplog.set_level(logging.INFO, logger="supriya")


@pytest.fixture
def two_voice_synthdef() -> SynthDef:
    with SynthDefBuilder(
        frequencies=(220, 440),
        amplitude=Parameter(value=1.0, rate=ParameterRate.AUDIO),
    ) as builder:
        sin_osc = SinOsc.ar(frequency=builder["frequencies"])
        enveloped_sin = sin_osc * builder["amplitude"]
        Out.ar(bus=0, source=enveloped_sin)
    return builder.build(name="test:two-voice")
