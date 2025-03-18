from uqbar.strings import normalize

from supriya.ugens import Mix, Out, SinOsc, SynthDefBuilder


def test_multi_value_parameters() -> None:
    with SynthDefBuilder(amp=0.1, freqs=[300, 400], out=0) as builder:
        sines = SinOsc.ar(frequency=builder["freqs"])
        sines = Mix.new(sines)
        sines = sines * builder["amp"]
        Out.ar(bus=builder["out"], source=sines)
    synthdef = builder.build()
    assert str(synthdef) == normalize(
        """
        synthdef:
            name: 58528261cb129f5bee634d41a34e082c
            ugens:
            -   Control.kr:
                    amp: 0.1
                    freqs[0]: 300.0
                    freqs[1]: 400.0
                    out: 0.0
            -   SinOsc.ar/0:
                    frequency: Control.kr[1:freqs[0]]
                    phase: 0.0
            -   SinOsc.ar/1:
                    frequency: Control.kr[2:freqs[1]]
                    phase: 0.0
            -   BinaryOpUGen(ADDITION).ar:
                    left: SinOsc.ar/0[0]
                    right: SinOsc.ar/1[0]
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: BinaryOpUGen(ADDITION).ar[0]
                    right: Control.kr[0:amp]
            -   Out.ar:
                    bus: Control.kr[3:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """
    )
