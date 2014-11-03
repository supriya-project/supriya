# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class StereoConvolution2L(MultiOutUGen):

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
        crossfade=1,
        framesize=2048,
        kernel_l=None,
        kernel_r=None,
        source=None,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel_l=kernel_l,
            kernel_r=kernel_r,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        crossfade=1,
        framesize=2048,
        kernel_l=None,
        kernel_r=None,
        source=None,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel_l=kernel_l,
            kernel_r=kernel_r,
            source=source,
            trigger=trigger,
            )
        return ugen
