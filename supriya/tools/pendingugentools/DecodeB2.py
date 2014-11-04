# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class DecodeB2(MultiOutUGen):

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
        num_chans=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            num_chans=num_chans,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        num_chans=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            num_chans=num_chans,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        num_chans=None,
        orientation=0.5,
        w=None,
        x=None,
        y=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            num_chans=num_chans,
            orientation=orientation,
            w=w,
            x=x,
            y=y,
            )
        return ugen
