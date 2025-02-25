import pytest
from uqbar.strings import normalize

from supriya.ugens import Rand, SinOsc, Sum3
from supriya.ugens.core import UGenRecursiveInput


@pytest.mark.parametrize(
    "input_one, input_two, input_three, expected",
    [
        (
            SinOsc.kr(),
            SinOsc.ar(),
            SinOsc.ar(),
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar/1:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   Sum3.ar:
                        input_one: SinOsc.ar/0[0]
                        input_two: SinOsc.ar/1[0]
                        input_three: SinOsc.kr[0]
            """,
        ),
        (
            Rand.ir(),
            SinOsc.ar(),
            SinOsc.kr(),
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
            SinOsc.kr(),
            SinOsc.ar(),
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: SinOsc.kr[0]
                        right: SinOsc.ar[0]
            """,
        ),
        (
            SinOsc.kr(),
            0,
            SinOsc.ar(),
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: SinOsc.kr[0]
                        right: SinOsc.ar[0]
            """,
        ),
        (
            SinOsc.kr(),
            SinOsc.ar(),
            0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.kr:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: SinOsc.kr[0]
                        right: SinOsc.ar[0]
            """,
        ),
    ],
)
def test_Sum3(
    input_one: UGenRecursiveInput,
    input_two: UGenRecursiveInput,
    input_three: UGenRecursiveInput,
    expected: str,
) -> None:
    result = Sum3.new(
        input_one=input_one,
        input_two=input_two,
        input_three=input_three,
    )
    assert normalize(str(result)) == normalize(expected)
