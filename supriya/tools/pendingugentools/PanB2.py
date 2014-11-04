# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PanB2(MultiOutUGen):

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
        azimuth=0,
        gain=1,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        azimuth=0,
        gain=1,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        azimuth=0,
        gain=1,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            source=source,
            )
        return ugen
