# -*- encoding: utf-8 -*-
import abc
from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class LinLin(PseudoUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @staticmethod
    def ar(
        source=None,
        in_min=0.0,
        in_max=1.0,
        out_min=1.0,
        out_max=2.0,
        ):
        from supriya.tools import ugentools
        scale = (out_max - out_min) / (in_max - in_min)
        offset = out_min - (scale * in_min)
        ugen = ugentools.MulAdd.new(
            source=source,
            multiplier=scale,
            addend=offset,
            )
        return ugen

    @staticmethod
    def kr(
        source=None,
        in_min=0.0,
        in_max=1.0,
        out_min=1.0,
        out_max=2.0,
        ):
        scale = (out_max - out_min) / (in_max - in_min)
        offset = out_min - (scale * in_min)
        ugen = (source * scale) + offset
        return ugen