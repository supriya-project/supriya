# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class VarLag(Filter):

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
        curvature=0,
        source=0,
        start=None,
        time=0.1,
        warp=5,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        curvature=0,
        source=0,
        start=None,
        time=0.1,
        warp=5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        curvature=0,
        source=0,
        start=None,
        time=0.1,
        warp=5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curvature=curvature,
            source=source,
            start=start,
            time=time,
            warp=warp,
            )
        return ugen

    # def new1(): ...
