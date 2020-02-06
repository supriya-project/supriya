import collections
import math

from supriya import CalculationRate
from supriya.ugens.Mix import Mix
from supriya.ugens.Pan2 import Pan2
from supriya.ugens.PseudoUGen import PseudoUGen
from supriya.synthdefs import UGen


class Splay(PseudoUGen):
    """
    A stereo signal spreader.

    ::

        >>> source = supriya.ugens.SinOsc.ar(frequency=[333, 444, 555, 666, 777])
        >>> splay = supriya.ugens.Splay.ar(source=source)
        >>> splay
        UGenArray({2})

    ::

        >>> print(splay)
        synthdef:
            name: ...
            ugens:
            -   SinOsc.ar/0:
                    frequency: 333.0
                    phase: 0.0
            -   Pan2.ar/0:
                    level: 1.0
                    position: -1.0
                    source: SinOsc.ar/0[0]
            -   SinOsc.ar/1:
                    frequency: 444.0
                    phase: 0.0
            -   Pan2.ar/1:
                    level: 1.0
                    position: -0.5
                    source: SinOsc.ar/1[0]
            -   SinOsc.ar/2:
                    frequency: 555.0
                    phase: 0.0
            -   Pan2.ar/2:
                    level: 1.0
                    position: 0.0
                    source: SinOsc.ar/2[0]
            -   SinOsc.ar/3:
                    frequency: 666.0
                    phase: 0.0
            -   Pan2.ar/3:
                    level: 1.0
                    position: 0.5
                    source: SinOsc.ar/3[0]
            -   Sum4.ar/0:
                    input_four: Pan2.ar/3[0]
                    input_one: Pan2.ar/0[0]
                    input_three: Pan2.ar/2[0]
                    input_two: Pan2.ar/1[0]
            -   Sum4.ar/1:
                    input_four: Pan2.ar/3[1]
                    input_one: Pan2.ar/0[1]
                    input_three: Pan2.ar/2[1]
                    input_two: Pan2.ar/1[1]
            -   SinOsc.ar/4:
                    frequency: 777.0
                    phase: 0.0
            -   Pan2.ar/4:
                    level: 1.0
                    position: 1.0
                    source: SinOsc.ar/4[0]
            -   BinaryOpUGen(ADDITION).ar/0:
                    left: Sum4.ar/0[0]
                    right: Pan2.ar/4[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: BinaryOpUGen(ADDITION).ar/0[0]
                    right: 0.4472135954999579
            -   BinaryOpUGen(ADDITION).ar/1:
                    left: Sum4.ar/1[0]
                    right: Pan2.ar/4[1]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(ADDITION).ar/1[0]
                    right: 0.4472135954999579

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Spatialization UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("spread", 1),
            ("level", 1),
            ("center", 0),
            ("normalize", True),
            ("source", None),
        ]
    )

    _unexpanded_input_names = ("source",)

    @classmethod
    def _new_expanded(cls, calculation_rate=None, **kwargs):
        dictionaries = UGen._expand_dictionary(
            kwargs, unexpanded_input_names=["source"]
        )
        ugens = [
            cls._new_single(calculation_rate=calculation_rate, **dictionary)
            for dictionary in dictionaries
        ]
        return Mix.multichannel(ugens, 2)

    @classmethod
    def _new_single(
        cls,
        calculation_rate=None,
        center=0,
        level=1,
        normalize=True,
        source=None,
        spread=1,
    ):
        positions = [
            (i * (2 / (len(source) - 1)) - 1) * spread + center
            for i in range(len(source))
        ]
        if normalize:
            if calculation_rate == CalculationRate.AUDIO:
                level = level * math.sqrt(1 / len(source))
            else:
                level = level / len(source)
        panners = UGen._get_method_for_rate(Pan2, calculation_rate)(
            source=source, position=positions
        )
        return Mix.multichannel(panners, 2) * level

    @classmethod
    def ar(cls, *, center=0, level=1, normalize=True, source=None, spread=1):
        return cls._new_expanded(
            calculation_rate=CalculationRate.AUDIO,
            center=center,
            level=level,
            normalize=normalize,
            source=source,
            spread=spread,
        )

    @classmethod
    def kr(cls, *, center=0, level=1, normalize=True, source=None, spread=1):
        return cls._new_expanded(
            calculation_rate=CalculationRate.CONTROL,
            center=center,
            level=level,
            normalize=normalize,
            source=source,
            spread=spread,
        )
