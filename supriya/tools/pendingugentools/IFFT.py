# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class IFFT(WidthFirstUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer=None,
        winsize=0,
        wintype=0,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer=buffer,
            winsize=winsize,
            wintype=wintype,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer=None,
        winsize=0,
        wintype=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer=None,
        winsize=0,
        wintype=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen

    @classmethod
    def new(
        cls,
        buffer=None,
        winsize=0,
        wintype=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer=buffer,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen
