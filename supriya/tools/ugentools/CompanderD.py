# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class CompanderD(PseudoUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Dynamics UGens'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=0.,
        thresh=0.5,
        clamp_time=0.01,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        ):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        rate = synthdeftools.Rate.AUDIO
        control = ugentools.DelayN.ar(
            source=source,
            maximum_delay_time=clamp_time,
            delay_time=clamp_time,
            )
        ugen = ugentools.Compander._new_expanded(
            clamp_time=clamp_time,
            rate=rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            control=control,
            thresh=thresh,
            )
        return ugen