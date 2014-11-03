# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class BiPanB2(MultiOutUGen):

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
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        azimuth=None,
        gain=1,
        in_a=None,
        in_b=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            in_a=in_a,
            in_b=in_b,
            )
        return ugen
