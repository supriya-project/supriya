# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Warp1(MultiOutUGen):

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
        bufnum=0,
        channel_count=1,
        envbufnum=-1,
        freq_scale=1,
        interp=1,
        overlaps=8,
        pointer=0,
        window_rand_ratio=0,
        window_size=0.2,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            envbufnum=envbufnum,
            freq_scale=freq_scale,
            interp=interp,
            overlaps=overlaps,
            pointer=pointer,
            window_rand_ratio=window_rand_ratio,
            window_size=window_size,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufnum=0,
        channel_count=1,
        envbufnum=-1,
        freq_scale=1,
        interp=1,
        overlaps=8,
        pointer=0,
        window_rand_ratio=0,
        window_size=0.2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            envbufnum=envbufnum,
            freq_scale=freq_scale,
            interp=interp,
            overlaps=overlaps,
            pointer=pointer,
            window_rand_ratio=window_rand_ratio,
            window_size=window_size,
            )
        return ugen
