# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Onsets(UGen):

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
        chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype='"rcomplex"',
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chain=chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        chain=None,
        floor=0.1,
        medianspan=11,
        mingap=10,
        odftype='"rcomplex"',
        rawodf=0,
        relaxtime=1,
        threshold=0.5,
        whtype=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chain=chain,
            floor=floor,
            medianspan=medianspan,
            mingap=mingap,
            odftype=odftype,
            rawodf=rawodf,
            relaxtime=relaxtime,
            threshold=threshold,
            whtype=whtype,
            )
        return ugen
