# flake8: noqa
import supriya.synthdefs
import supriya.ugens


def test_SynthDefCompiler_optimization_01():

    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        "optimized",
        r"""
        var sine_a, sine_b, sine_c, sine_d;
        sine_a = SinOsc.ar(420);
        sine_b = SinOsc.ar(440);
        sine_c = SinOsc.ar(460);
        sine_d = SinOsc.ar(sine_c);
        Out.ar(0, sine_a);
        """,
    )
    sc_compiled_synthdef = bytes(sc_synthdef.compile())

    with supriya.synthdefs.SynthDefBuilder() as builder:
        sine_a = supriya.ugens.SinOsc.ar(frequency=420)
        sine_b = supriya.ugens.SinOsc.ar(frequency=440)  # noqa
        sine_c = supriya.ugens.SinOsc.ar(frequency=460)
        sine_d = supriya.ugens.SinOsc.ar(frequency=sine_c)  # noqa
        supriya.ugens.Out.ar(bus=0, source=sine_a)
    py_synthdef = builder.build("optimized")
    py_compiled_synthdef = py_synthdef.compile()

    # fmt: off
    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\toptimized'
                b'\x00\x00\x00\x02'
                    b'C\xd2\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x02'
                    b'\x06SinOsc'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                b'\x00\x00'
    )
    # fmt: on

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef
