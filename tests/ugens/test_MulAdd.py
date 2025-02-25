import pytest
from uqbar.strings import normalize

from supriya.ugens import DC, MulAdd, Rand, SinOsc


@pytest.mark.parametrize(
    "source, multiplier, addend, expected",
    [
        (
            SinOsc.ar(),
            SinOsc.kr(),
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
                -   MulAdd.ar:
                        source: SinOsc.ar[0]
                        multiplier: SinOsc.kr[0]
                        addend: Rand.ir[0]
            """,
        ),
        (
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
                -   MulAdd.ar:
                        source: SinOsc.ar[0]
                        multiplier: SinOsc.kr[0]
                        addend: Rand.ir[0]
            """,
        ),
        (
            SinOsc.kr(),
            Rand.ir(),
            SinOsc.ar(),
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
                -   BinaryOpUGen(MULTIPLICATION).kr:
                        left: SinOsc.kr[0]
                        right: Rand.ir[0]
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: BinaryOpUGen(MULTIPLICATION).kr[0]
                        right: SinOsc.ar[0]
            """,
        ),
        (
            SinOsc.kr(),
            Rand.ir(),
            DC.kr(source=1.23),
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
                -   DC.kr:
                        source: 1.23
                -   MulAdd.kr:
                        source: SinOsc.kr[0]
                        multiplier: Rand.ir[0]
                        addend: DC.kr[0]
            """,
        ),
        (
            SinOsc.ar(),
            0,
            Rand.ir(),
            """
            synthdef:
                name: ...
                ugens:
                -   Rand.ir:
                        minimum: 0.0
                        maximum: 1.0
            """,
        ),
        (
            SinOsc.ar(),
            -1,
            Rand.ir(),
            """
            synthdef:
                name: ...
                ugens:
                -   Rand.ir:
                        minimum: 0.0
                        maximum: 1.0
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(SUBTRACTION).ar:
                        left: Rand.ir[0]
                        right: SinOsc.ar[0]
            """,
        ),
        (
            SinOsc.ar(),
            1,
            Rand.ir(),
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
        (
            SinOsc.ar(),
            1,
            0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
            """,
        ),
        (
            SinOsc.ar(),
            -1,
            0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   UnaryOpUGen(NEGATIVE).ar:
                        source: SinOsc.ar[0]
            """,
        ),
        (
            SinOsc.ar(),
            23,
            0,
            """
            synthdef:
                name: ...
                ugens:
                -   SinOsc.ar:
                        frequency: 440.0
                        phase: 0.0
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: SinOsc.ar[0]
                        right: 23.0
            """,
        ),
    ],
)
def test_MulAdd(source, multiplier, addend, expected) -> None:
    result = MulAdd.new(source=source, multiplier=multiplier, addend=addend)
    assert normalize(str(result)) == normalize(expected)
