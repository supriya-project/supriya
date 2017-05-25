# -*- encoding: utf-8 -*-
from supriya.tools import synthdeftools
from supriya.tools import ugentools


def test_SynthDefCompiler_ambisonics_01():

    sc_synthdef = synthdeftools.SuperColliderSynthDef(
        'ambisonics',
        r"""
        var source, azimuth, w, x, y;
        source = PinkNoise.ar();
        azimuth = LFNoise2.kr(0.25);
        #w, x, y = PanB2.ar(source, azimuth, 1);
        source = DecodeB2.ar(4, w, x, y, 0.5);
        Out.ar(0, source);
        """
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    with synthdeftools.SynthDefBuilder() as builder:
        source = ugentools.PinkNoise.ar()
        azimuth = ugentools.LFNoise2.kr(frequency=0.25)
        w, x, y = ugentools.PanB2.ar(source=source, azimuth=azimuth)
        source = ugentools.DecodeB2.ar(
            channel_count=4, w=w, x=x, y=y, orientation=0.5)
        ugentools.Out.ar(0, source)
    py_synthdef = builder.build('ambisonics')
    py_compiled_synthdef = py_synthdef.compile()

    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\nambisonics'
                b'\x00\x00\x00\x04'
                    b'>\x80\x00\x00'
                    b'?\x80\x00\x00'
                    b'?\x00\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x05'
                    b'\tPinkNoise'
                        b'\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x02'
                    b'\x08LFNoise2'
                        b'\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x00'
                            b'\x01'
                    b'\x05PanB2'
                        b'\x02'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00\x00\x03'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                                b'\x00\x00\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x01'
                            b'\x02'
                            b'\x02'
                            b'\x02'
                    b'\x08DecodeB2'
                        b'\x02'
                        b'\x00\x00\x00\x04'
                        b'\x00\x00\x00\x04'
                        b'\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x02'
                                b'\x00\x00\x00\x02'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x02'
                            b'\x02'
                            b'\x02'
                            b'\x02'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x05'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                                b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x02'
                            b'\x00\x00\x00\x03'
                                b'\x00\x00\x00\x03'
                b'\x00\x00'
        )

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef