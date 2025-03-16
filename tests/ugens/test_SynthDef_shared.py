import pytest

import supriya.ugens
from supriya import SynthDefBuilder
from supriya.ugens.core import SynthDefError


def test_01() -> None:
    """
    Cannot share UGens.
    """

    with SynthDefBuilder():
        sine_one = supriya.ugens.SinOsc.ar()
        supriya.ugens.Out.ar(bus=0, source=sine_one)

    with SynthDefBuilder():
        sine_two = supriya.ugens.SinOsc.ar()
        with pytest.raises(SynthDefError) as exception_info:
            sine_two * sine_one
        assert "UGen input in different scope" in str(exception_info.value)


def test_02() -> None:
    """
    Cannot share parameters.
    """

    with SynthDefBuilder(bus=0) as builder:
        sine_one = supriya.ugens.SinOsc.ar()
        synth_one_bus = builder["bus"]
        supriya.ugens.Out.ar(bus=synth_one_bus, source=sine_one)

    with SynthDefBuilder():
        sine_two = supriya.ugens.SinOsc.ar()
        with pytest.raises(SynthDefError) as exception_info:
            supriya.ugens.Out.ar(bus=synth_one_bus, source=sine_two)
        assert "UGen input in different scope" in str(exception_info.value)


def test_03() -> None:
    """
    Cannot share output proxies.
    """
    with SynthDefBuilder():
        left, right = supriya.ugens.SinOsc.ar(frequency=[440, 442])
        supriya.ugens.Out.ar(bus=0, source=[right, left])

    with SynthDefBuilder():
        with pytest.raises(SynthDefError) as exception_info:
            left * right
        assert "UGen input in different scope" in str(exception_info.value)
