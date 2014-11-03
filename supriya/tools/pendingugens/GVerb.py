# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class GVerb(MultiOutUGen):

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
        damping=0.5,
        drylevel=1,
        earlyreflevel=0.7,
        inputbw=0.5,
        maxroomsize=300,
        revtime=3,
        roomsize=10,
        source=None,
        spread=15,
        taillevel=0.5,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            drylevel=drylevel,
            earlyreflevel=earlyreflevel,
            inputbw=inputbw,
            maxroomsize=maxroomsize,
            revtime=revtime,
            roomsize=roomsize,
            source=source,
            spread=spread,
            taillevel=taillevel,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0.5,
        drylevel=1,
        earlyreflevel=0.7,
        inputbw=0.5,
        maxroomsize=300,
        revtime=3,
        roomsize=10,
        source=None,
        spread=15,
        taillevel=0.5,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            drylevel=drylevel,
            earlyreflevel=earlyreflevel,
            inputbw=inputbw,
            maxroomsize=maxroomsize,
            revtime=revtime,
            roomsize=roomsize,
            source=source,
            spread=spread,
            taillevel=taillevel,
            )
        return ugen
