# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Compander(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'control',
        'thresh',
        'slope_below',
        'slope_above',
        'clamp_time',
        'relax_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        clamp_time=0.01,
        control=0.,
        rate=None,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        source=0.,
        thresh=0.5,
        ):
        UGen.__init__(
            self,
            clamp_time=clamp_time,
            control=control,
            rate=rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            thresh=thresh,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        clamp_time=0.01,
        control=0.,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        source=0.,
        thresh=0.5,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            clamp_time=clamp_time,
            control=control,
            rate=rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            thresh=thresh,
            )
        return ugen