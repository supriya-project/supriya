import abc
import collections
from supriya import CalculationRate
from supriya.ugens.PseudoUGen import PseudoUGen


class LinLin(PseudoUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @staticmethod
    def ar(
        source=None,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
        ):
        import supriya.ugens
        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        ugen = supriya.ugens.MulAdd.new(
            source=source,
            multiplier=scale,
            addend=offset,
            )
        return ugen

    @staticmethod
    def kr(
        source=None,
        input_minimum=0.0,
        input_maximum=1.0,
        output_minimum=1.0,
        output_maximum=2.0,
        ):
        import supriya.ugens
        scale = (output_maximum - output_minimum) / (input_maximum - input_minimum)
        offset = output_minimum - (scale * input_minimum)
        ugen = supriya.ugens.MulAdd.new(
            source=source,
            multiplier=scale,
            addend=offset,
            )
        return ugen
