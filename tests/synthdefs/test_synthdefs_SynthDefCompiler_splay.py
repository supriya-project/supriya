import platform

import pytest
from uqbar.strings import normalize

import supriya.synthdefs
import supriya.ugens


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_Splay_01_sclang(server):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "test",
        r"""
        arg spread=1, level=0.2, center=0.0;
        Out.ar(0, Splay.ar(In.ar(0, 5), spread, level, center));
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    synthdef = supriya.synthdefs.SynthDefDecompiler.decompile_synthdefs(
        sc_compiled_synthdef
    )[0]
    assert normalize(str(synthdef)) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.kr: null
            -   BinaryOpUGen(SUBTRACTION).kr:
                    left: Control.kr[2:center]
                    right: Control.kr[0:spread]
            -   MulAdd.kr/0:
                    source: Control.kr[0:spread]
                    multiplier: -0.5
                    addend: Control.kr[2:center]
            -   MulAdd.kr/1:
                    source: Control.kr[0:spread]
                    multiplier: 0.5
                    addend: Control.kr[2:center]
            -   BinaryOpUGen(ADDITION).kr:
                    left: Control.kr[0:spread]
                    right: Control.kr[2:center]
            -   BinaryOpUGen(MULTIPLICATION).kr:
                    left: Control.kr[1:level]
                    right: 0.4472135901451111
            -   In.ar:
                    bus: 0.0
            -   Pan2.ar/0:
                    source: In.ar[0]
                    position: BinaryOpUGen(SUBTRACTION).kr[0]
                    level: 1.0
            -   Pan2.ar/1:
                    source: In.ar[1]
                    position: MulAdd.kr/0[0]
                    level: 1.0
            -   Pan2.ar/2:
                    source: In.ar[2]
                    position: Control.kr[2:center]
                    level: 1.0
            -   Pan2.ar/3:
                    source: In.ar[3]
                    position: MulAdd.kr/1[0]
                    level: 1.0
            -   Sum4.ar/0:
                    input_one: Pan2.ar/3[0]
                    input_two: Pan2.ar/2[0]
                    input_three: Pan2.ar/1[0]
                    input_four: Pan2.ar/0[0]
            -   Sum4.ar/1:
                    input_one: Pan2.ar/3[1]
                    input_two: Pan2.ar/2[1]
                    input_three: Pan2.ar/1[1]
                    input_four: Pan2.ar/0[1]
            -   Pan2.ar/4:
                    source: In.ar[4]
                    position: BinaryOpUGen(ADDITION).kr[0]
                    level: 1.0
            -   BinaryOpUGen(ADDITION).ar/0:
                    left: Sum4.ar/0[0]
                    right: Pan2.ar/4[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: BinaryOpUGen(ADDITION).ar/0[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr[0]
            -   BinaryOpUGen(ADDITION).ar/1:
                    left: Sum4.ar/1[0]
                    right: Pan2.ar/4[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(ADDITION).ar/1[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
        """
    )


def test_Splay_01_supriya(server):
    with supriya.synthdefs.SynthDefBuilder(spread=1, level=0.2, center=0.0) as builder:
        source = supriya.ugens.Splay.ar(
            source=supriya.ugens.In.ar(bus=0, channel_count=5),
            spread=builder["spread"],
            level=builder["level"],
            center=builder["center"],
        )
        supriya.ugens.Out.ar(bus=0, source=source)
    py_synthdef = builder.build(name="test")
    assert normalize(str(py_synthdef)) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.kr: null
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: -1.0
                    right: Control.kr[2:spread]
            -   BinaryOpUGen(ADDITION).kr/0:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Control.kr[0:center]
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: -0.5
                    right: Control.kr[2:spread]
            -   BinaryOpUGen(ADDITION).kr/1:
                    left: BinaryOpUGen(MULTIPLICATION).kr/1[0]
                    right: Control.kr[0:center]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: 0.5
                    right: Control.kr[2:spread]
            -   BinaryOpUGen(ADDITION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                    right: Control.kr[0:center]
            -   BinaryOpUGen(ADDITION).kr/3:
                    left: Control.kr[2:spread]
                    right: Control.kr[0:center]
            -   BinaryOpUGen(MULTIPLICATION).kr/3:
                    left: Control.kr[1:level]
                    right: 0.4472135954999579
            -   In.ar:
                    bus: 0.0
            -   Pan2.ar/0:
                    source: In.ar[0]
                    position: BinaryOpUGen(ADDITION).kr/0[0]
                    level: 1.0
            -   Pan2.ar/1:
                    source: In.ar[1]
                    position: BinaryOpUGen(ADDITION).kr/1[0]
                    level: 1.0
            -   Pan2.ar/2:
                    source: In.ar[2]
                    position: Control.kr[0:center]
                    level: 1.0
            -   Pan2.ar/3:
                    source: In.ar[3]
                    position: BinaryOpUGen(ADDITION).kr/2[0]
                    level: 1.0
            -   Sum4.ar/0:
                    input_one: Pan2.ar/0[0]
                    input_two: Pan2.ar/1[0]
                    input_three: Pan2.ar/2[0]
                    input_four: Pan2.ar/3[0]
            -   Sum4.ar/1:
                    input_one: Pan2.ar/0[1]
                    input_two: Pan2.ar/1[1]
                    input_three: Pan2.ar/2[1]
                    input_four: Pan2.ar/3[1]
            -   Pan2.ar/4:
                    source: In.ar[4]
                    position: BinaryOpUGen(ADDITION).kr/3[0]
                    level: 1.0
            -   BinaryOpUGen(ADDITION).ar/0:
                    left: Sum4.ar/0[0]
                    right: Pan2.ar/4[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: BinaryOpUGen(ADDITION).ar/0[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/3[0]
            -   BinaryOpUGen(ADDITION).ar/1:
                    left: Sum4.ar/1[0]
                    right: Pan2.ar/4[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(ADDITION).ar/1[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/3[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
        """
    )
    py_synthdef.allocate(server=server)


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
def test_Splay_02_sclang(server):
    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "test",
        r"""
        arg spread=1, level=0.2;
        Out.ar(0, Splay.ar(In.ar(0, 5), spread, level, [-0.25, 0.25]));
        """,
    )
    sc_compiled_synthdef = sc_synthdef.compile()
    synthdef = supriya.synthdefs.SynthDefDecompiler.decompile_synthdefs(
        sc_compiled_synthdef
    )[0]
    assert normalize(str(synthdef)) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.kr: null
            -   BinaryOpUGen(SUBTRACTION).kr/0:
                    left: -0.25
                    right: Control.kr[0:spread]
            -   MulAdd.kr/0:
                    source: Control.kr[0:spread]
                    multiplier: -0.5
                    addend: -0.25
            -   MulAdd.kr/1:
                    source: Control.kr[0:spread]
                    multiplier: 0.5
                    addend: -0.25
            -   BinaryOpUGen(ADDITION).kr/0:
                    left: Control.kr[0:spread]
                    right: -0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Control.kr[1:level]
                    right: 0.4472135901451111
            -   BinaryOpUGen(SUBTRACTION).kr/1:
                    left: 0.25
                    right: Control.kr[0:spread]
            -   MulAdd.kr/2:
                    source: Control.kr[0:spread]
                    multiplier: -0.5
                    addend: 0.25
            -   MulAdd.kr/3:
                    source: Control.kr[0:spread]
                    multiplier: 0.5
                    addend: 0.25
            -   BinaryOpUGen(ADDITION).kr/1:
                    left: Control.kr[0:spread]
                    right: 0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: Control.kr[1:level]
                    right: 0.4472135901451111
            -   In.ar:
                    bus: 0.0
            -   Pan2.ar/0:
                    source: In.ar[0]
                    position: BinaryOpUGen(SUBTRACTION).kr/0[0]
                    level: 1.0
            -   Pan2.ar/1:
                    source: In.ar[1]
                    position: MulAdd.kr/0[0]
                    level: 1.0
            -   Pan2.ar/2:
                    source: In.ar[2]
                    position: -0.25
                    level: 1.0
            -   Pan2.ar/3:
                    source: In.ar[3]
                    position: MulAdd.kr/1[0]
                    level: 1.0
            -   Sum4.ar/0:
                    input_one: Pan2.ar/3[0]
                    input_two: Pan2.ar/2[0]
                    input_three: Pan2.ar/1[0]
                    input_four: Pan2.ar/0[0]
            -   Sum4.ar/1:
                    input_one: Pan2.ar/3[1]
                    input_two: Pan2.ar/2[1]
                    input_three: Pan2.ar/1[1]
                    input_four: Pan2.ar/0[1]
            -   Pan2.ar/4:
                    source: In.ar[4]
                    position: BinaryOpUGen(ADDITION).kr/0[0]
                    level: 1.0
            -   BinaryOpUGen(ADDITION).ar/0:
                    left: Sum4.ar/0[0]
                    right: Pan2.ar/4[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: BinaryOpUGen(ADDITION).ar/0[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/0[0]
            -   BinaryOpUGen(ADDITION).ar/1:
                    left: Sum4.ar/1[0]
                    right: Pan2.ar/4[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(ADDITION).ar/1[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/0[0]
            -   Pan2.ar/5:
                    source: In.ar[0]
                    position: BinaryOpUGen(SUBTRACTION).kr/1[0]
                    level: 1.0
            -   Pan2.ar/6:
                    source: In.ar[1]
                    position: MulAdd.kr/2[0]
                    level: 1.0
            -   Pan2.ar/7:
                    source: In.ar[2]
                    position: 0.25
                    level: 1.0
            -   Pan2.ar/8:
                    source: In.ar[3]
                    position: MulAdd.kr/3[0]
                    level: 1.0
            -   Sum4.ar/2:
                    input_one: Pan2.ar/8[0]
                    input_two: Pan2.ar/7[0]
                    input_three: Pan2.ar/6[0]
                    input_four: Pan2.ar/5[0]
            -   Sum4.ar/3:
                    input_one: Pan2.ar/8[1]
                    input_two: Pan2.ar/7[1]
                    input_three: Pan2.ar/6[1]
                    input_four: Pan2.ar/5[1]
            -   Pan2.ar/9:
                    source: In.ar[4]
                    position: BinaryOpUGen(ADDITION).kr/1[0]
                    level: 1.0
            -   BinaryOpUGen(ADDITION).ar/2:
                    left: Sum4.ar/2[0]
                    right: Pan2.ar/9[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: BinaryOpUGen(ADDITION).ar/2[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   Out.ar/0:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
            -   BinaryOpUGen(ADDITION).ar/3:
                    left: Sum4.ar/3[0]
                    right: Pan2.ar/9[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/3:
                    left: BinaryOpUGen(ADDITION).ar/3[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   Out.ar/1:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
        """
    )


def test_Splay_02_supriya(server):
    with supriya.synthdefs.SynthDefBuilder(spread=1, level=0.2) as builder:
        source = supriya.ugens.Splay.ar(
            source=supriya.ugens.In.ar(bus=0, channel_count=5),
            spread=builder["spread"],
            level=builder["level"],
            center=[-0.25, 0.25],
        )
        supriya.ugens.Out.ar(bus=0, source=source)
    py_synthdef = builder.build(name="test")
    assert normalize(str(py_synthdef)) == normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.kr: null
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: -1.0
                    right: Control.kr[1:spread]
            -   BinaryOpUGen(ADDITION).kr/0:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: -0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: -0.5
                    right: Control.kr[1:spread]
            -   BinaryOpUGen(ADDITION).kr/1:
                    left: BinaryOpUGen(MULTIPLICATION).kr/1[0]
                    right: -0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: 0.5
                    right: Control.kr[1:spread]
            -   BinaryOpUGen(ADDITION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                    right: -0.25
            -   BinaryOpUGen(ADDITION).kr/3:
                    left: Control.kr[1:spread]
                    right: -0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/3:
                    left: Control.kr[0:level]
                    right: 0.4472135954999579
            -   BinaryOpUGen(MULTIPLICATION).kr/4:
                    left: -1.0
                    right: Control.kr[1:spread]
            -   BinaryOpUGen(ADDITION).kr/4:
                    left: BinaryOpUGen(MULTIPLICATION).kr/4[0]
                    right: 0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/5:
                    left: -0.5
                    right: Control.kr[1:spread]
            -   BinaryOpUGen(ADDITION).kr/5:
                    left: BinaryOpUGen(MULTIPLICATION).kr/5[0]
                    right: 0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/6:
                    left: 0.5
                    right: Control.kr[1:spread]
            -   BinaryOpUGen(ADDITION).kr/6:
                    left: BinaryOpUGen(MULTIPLICATION).kr/6[0]
                    right: 0.25
            -   BinaryOpUGen(ADDITION).kr/7:
                    left: Control.kr[1:spread]
                    right: 0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/7:
                    left: Control.kr[0:level]
                    right: 0.4472135954999579
            -   In.ar:
                    bus: 0.0
            -   Pan2.ar/0:
                    source: In.ar[0]
                    position: BinaryOpUGen(ADDITION).kr/0[0]
                    level: 1.0
            -   Pan2.ar/1:
                    source: In.ar[1]
                    position: BinaryOpUGen(ADDITION).kr/1[0]
                    level: 1.0
            -   Pan2.ar/2:
                    source: In.ar[2]
                    position: -0.25
                    level: 1.0
            -   Pan2.ar/3:
                    source: In.ar[3]
                    position: BinaryOpUGen(ADDITION).kr/2[0]
                    level: 1.0
            -   Sum4.ar/0:
                    input_one: Pan2.ar/0[0]
                    input_two: Pan2.ar/1[0]
                    input_three: Pan2.ar/2[0]
                    input_four: Pan2.ar/3[0]
            -   Sum4.ar/1:
                    input_one: Pan2.ar/0[1]
                    input_two: Pan2.ar/1[1]
                    input_three: Pan2.ar/2[1]
                    input_four: Pan2.ar/3[1]
            -   Pan2.ar/4:
                    source: In.ar[4]
                    position: BinaryOpUGen(ADDITION).kr/3[0]
                    level: 1.0
            -   BinaryOpUGen(ADDITION).ar/0:
                    left: Sum4.ar/0[0]
                    right: Pan2.ar/4[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: BinaryOpUGen(ADDITION).ar/0[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/3[0]
            -   BinaryOpUGen(ADDITION).ar/1:
                    left: Sum4.ar/1[0]
                    right: Pan2.ar/4[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(ADDITION).ar/1[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/3[0]
            -   Pan2.ar/5:
                    source: In.ar[0]
                    position: BinaryOpUGen(ADDITION).kr/4[0]
                    level: 1.0
            -   Pan2.ar/6:
                    source: In.ar[1]
                    position: BinaryOpUGen(ADDITION).kr/5[0]
                    level: 1.0
            -   Pan2.ar/7:
                    source: In.ar[2]
                    position: 0.25
                    level: 1.0
            -   Pan2.ar/8:
                    source: In.ar[3]
                    position: BinaryOpUGen(ADDITION).kr/6[0]
                    level: 1.0
            -   Sum4.ar/2:
                    input_one: Pan2.ar/5[0]
                    input_two: Pan2.ar/6[0]
                    input_three: Pan2.ar/7[0]
                    input_four: Pan2.ar/8[0]
            -   Sum4.ar/3:
                    input_one: Pan2.ar/5[1]
                    input_two: Pan2.ar/6[1]
                    input_three: Pan2.ar/7[1]
                    input_four: Pan2.ar/8[1]
            -   Pan2.ar/9:
                    source: In.ar[4]
                    position: BinaryOpUGen(ADDITION).kr/7[0]
                    level: 1.0
            -   BinaryOpUGen(ADDITION).ar/2:
                    left: Sum4.ar/2[0]
                    right: Pan2.ar/9[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: BinaryOpUGen(ADDITION).ar/2[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/7[0]
            -   BinaryOpUGen(ADDITION).ar/3:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: BinaryOpUGen(MULTIPLICATION).ar/2[0]
            -   BinaryOpUGen(ADDITION).ar/4:
                    left: Sum4.ar/3[0]
                    right: Pan2.ar/9[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/3:
                    left: BinaryOpUGen(ADDITION).ar/4[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/7[0]
            -   BinaryOpUGen(ADDITION).ar/5:
                    left: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    right: BinaryOpUGen(MULTIPLICATION).ar/3[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(ADDITION).ar/3[0]
                    source[1]: BinaryOpUGen(ADDITION).ar/5[0]
        """
    )
    py_synthdef.allocate(server=server)
