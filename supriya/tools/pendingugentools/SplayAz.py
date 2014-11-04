# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SplayAz(UGen):

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
        center=0,
        in_array=None,
        level=1,
        level_comp=True,
        num_chans=4,
        orientation=0.5,
        spread=1,
        width=2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            center=center,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            num_chans=num_chans,
            orientation=orientation,
            spread=spread,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        center=0,
        in_array=None,
        level=1,
        level_comp=True,
        num_chans=4,
        orientation=0.5,
        spread=1,
        width=2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            num_chans=num_chans,
            orientation=orientation,
            spread=spread,
            width=width,
            )
        return ugen

    # def arFill(): ...

    @classmethod
    def kr(
        cls,
        center=0,
        in_array=None,
        level=1,
        level_comp=True,
        num_chans=4,
        orientation=0.5,
        spread=1,
        width=2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            num_chans=num_chans,
            orientation=orientation,
            spread=spread,
            width=width,
            )
        return ugen
