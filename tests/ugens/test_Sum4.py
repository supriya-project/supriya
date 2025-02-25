import pytest
from uqbar.strings import normalize

from supriya.ugens import Rand, SinOsc, Sum4
from supriya.ugens.core import UGenRecursiveInput


@pytest.mark.parametrize(
    "input_one, input_two, input_three, input_four, expected",
    [
        (
            1.0,
            SinOsc.kr(),
            SinOsc.ar(),
            Rand.ir(),
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   Rand.ir:
                        minimum: 0.0
                        maximum: 1.0
                -   Sum4.ar:
                        input_one: SinOsc.ar[0]
                        input_two: SinOsc.kr[0]
                        input_three: 1.0
                        input_four: Rand.ir[0]
            """,
        ),
        (
            0,
            SinOsc.ar(),
            Rand.ir(),
            1.0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   Rand.ir:
                        minimum: 0.0
                        maximum: 1.0
                -   Sum3.ar:
                        input_one: SinOsc.ar[0]
                        input_two: Rand.ir[0]
                        input_three: 1.0
            """,
        ),
        (
            SinOsc.kr(),
            0,
            Rand.ir(),
            1.0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   Rand.ir:
                        minimum: 0.0
                        maximum: 1.0
                -   Sum3.kr:
                        input_one: SinOsc.kr[0]
                        input_two: Rand.ir[0]
                        input_three: 1.0
            """,
        ),
        (
            SinOsc.kr(),
            SinOsc.ar(),
            0,
            1.0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   Sum3.ar:
                        input_one: SinOsc.ar[0]
                        input_two: SinOsc.kr[0]
                        input_three: 1.0
            """,
        ),
        (
            SinOsc.kr(),
            SinOsc.ar(),
            Rand.ir(),
            0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   Rand.ir:
                        minimum: 0.0
                        maximum: 1.0
                -   Sum3.ar:
                        input_one: SinOsc.ar[0]
                        input_two: SinOsc.kr[0]
                        input_three: Rand.ir[0]
            """,
        ),
        (
            0,
            SinOsc.ar(),
            Rand.ir(),
            0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   Rand.ir:
                        minimum: 0.0
                        maximum: 1.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: SinOsc.ar[0]
                        right: Rand.ir[0]
            """,
        ),
    ],
)
def test_Sum4(
    input_one: UGenRecursiveInput,
    input_two: UGenRecursiveInput,
    input_three: UGenRecursiveInput,
    input_four: UGenRecursiveInput,
    expected: str,
) -> None:
    result = Sum4.new(
        input_one=input_one,
        input_two=input_two,
        input_three=input_three,
        input_four=input_four,
    )
    assert normalize(str(result)) == normalize(expected)
