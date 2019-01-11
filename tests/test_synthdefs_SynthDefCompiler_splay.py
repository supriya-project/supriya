import uqbar.strings

import supriya.synthdefs
import supriya.ugens


def test_Splay_01():
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
    # supriya.graph(synthdef)
    assert uqbar.strings.normalize(str(synthdef)) == uqbar.strings.normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.kr: null
            -   BinaryOpUGen(SUBTRACTION).kr:
                    left: Control.kr[2:center]
                    right: Control.kr[0:spread]
            -   MulAdd.kr/0:
                    addend: Control.kr[2:center]
                    multiplier: -0.5
                    source: Control.kr[0:spread]
            -   MulAdd.kr/1:
                    addend: Control.kr[2:center]
                    multiplier: 0.5
                    source: Control.kr[0:spread]
            -   BinaryOpUGen(ADDITION).kr:
                    left: Control.kr[0:spread]
                    right: Control.kr[2:center]
            -   BinaryOpUGen(MULTIPLICATION).kr:
                    left: Control.kr[1:level]
                    right: 0.4472135901451111
            -   In.ar:
                    bus: 0.0
            -   Pan2.ar/0:
                    level: 1.0
                    position: BinaryOpUGen(SUBTRACTION).kr[0]
                    source: In.ar[0]
            -   Pan2.ar/1:
                    level: 1.0
                    position: MulAdd.kr/0[0]
                    source: In.ar[1]
            -   Pan2.ar/2:
                    level: 1.0
                    position: Control.kr[2:center]
                    source: In.ar[2]
            -   Pan2.ar/3:
                    level: 1.0
                    position: MulAdd.kr/1[0]
                    source: In.ar[3]
            -   Sum4.ar/0:
                    input_four: Pan2.ar/0[0]
                    input_one: Pan2.ar/3[0]
                    input_three: Pan2.ar/1[0]
                    input_two: Pan2.ar/2[0]
            -   Sum4.ar/1:
                    input_four: Pan2.ar/0[1]
                    input_one: Pan2.ar/3[1]
                    input_three: Pan2.ar/1[1]
                    input_two: Pan2.ar/2[1]
            -   Pan2.ar/4:
                    level: 1.0
                    position: BinaryOpUGen(ADDITION).kr[0]
                    source: In.ar[4]
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
    with supriya.synthdefs.SynthDefBuilder(spread=1, level=0.2, center=0.0) as builder:
        source = supriya.ugens.Splay.ar(
            source=supriya.ugens.In.ar(bus=0, channel_count=5),
            spread=builder["spread"],
            level=builder["level"],
            center=builder["center"],
        )
        supriya.ugens.Out.ar(bus=0, source=source)
    py_synthdef = builder.build(name="test")
    py_compiled_synthdef = py_synthdef.compile()


def test_Splay_02():
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
    # supriya.graph(synthdef)
    assert uqbar.strings.normalize(str(synthdef)) == uqbar.strings.normalize(
        """
        synthdef:
            name: test
            ugens:
            -   Control.kr: null
            -   BinaryOpUGen(SUBTRACTION).kr/0:
                    left: -0.25
                    right: Control.kr[0:spread]
            -   MulAdd.kr/0:
                    addend: -0.25
                    multiplier: -0.5
                    source: Control.kr[0:spread]
            -   MulAdd.kr/1:
                    addend: -0.25
                    multiplier: 0.5
                    source: Control.kr[0:spread]
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
                    addend: 0.25
                    multiplier: -0.5
                    source: Control.kr[0:spread]
            -   MulAdd.kr/3:
                    addend: 0.25
                    multiplier: 0.5
                    source: Control.kr[0:spread]
            -   BinaryOpUGen(ADDITION).kr/1:
                    left: Control.kr[0:spread]
                    right: 0.25
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: Control.kr[1:level]
                    right: 0.4472135901451111
            -   In.ar:
                    bus: 0.0
            -   Pan2.ar/0:
                    level: 1.0
                    position: BinaryOpUGen(SUBTRACTION).kr/0[0]
                    source: In.ar[0]
            -   Pan2.ar/1:
                    level: 1.0
                    position: MulAdd.kr/0[0]
                    source: In.ar[1]
            -   Pan2.ar/2:
                    level: 1.0
                    position: -0.25
                    source: In.ar[2]
            -   Pan2.ar/3:
                    level: 1.0
                    position: MulAdd.kr/1[0]
                    source: In.ar[3]
            -   Sum4.ar/0:
                    input_four: Pan2.ar/0[0]
                    input_one: Pan2.ar/3[0]
                    input_three: Pan2.ar/1[0]
                    input_two: Pan2.ar/2[0]
            -   Sum4.ar/1:
                    input_four: Pan2.ar/0[1]
                    input_one: Pan2.ar/3[1]
                    input_three: Pan2.ar/1[1]
                    input_two: Pan2.ar/2[1]
            -   Pan2.ar/4:
                    level: 1.0
                    position: BinaryOpUGen(ADDITION).kr/0[0]
                    source: In.ar[4]
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
                    level: 1.0
                    position: BinaryOpUGen(SUBTRACTION).kr/1[0]
                    source: In.ar[0]
            -   Pan2.ar/6:
                    level: 1.0
                    position: MulAdd.kr/2[0]
                    source: In.ar[1]
            -   Pan2.ar/7:
                    level: 1.0
                    position: 0.25
                    source: In.ar[2]
            -   Pan2.ar/8:
                    level: 1.0
                    position: MulAdd.kr/3[0]
                    source: In.ar[3]
            -   Sum4.ar/2:
                    input_four: Pan2.ar/5[0]
                    input_one: Pan2.ar/8[0]
                    input_three: Pan2.ar/6[0]
                    input_two: Pan2.ar/7[0]
            -   Sum4.ar/3:
                    input_four: Pan2.ar/5[1]
                    input_one: Pan2.ar/8[1]
                    input_three: Pan2.ar/6[1]
                    input_two: Pan2.ar/7[1]
            -   Pan2.ar/9:
                    level: 1.0
                    position: BinaryOpUGen(ADDITION).kr/1[0]
                    source: In.ar[4]
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
    # supriya.graph(synthdef)
    with supriya.synthdefs.SynthDefBuilder(spread=1, level=0.2) as builder:
        source = supriya.ugens.Splay.ar(
            source=supriya.ugens.In.ar(bus=0, channel_count=5),
            spread=builder["spread"],
            level=builder["level"],
            center=[-0.25, 0.25],
        )
        supriya.ugens.Out.ar(bus=0, source=source)
    py_synthdef = builder.build(name="test")
    py_compiled_synthdef = py_synthdef.compile()
