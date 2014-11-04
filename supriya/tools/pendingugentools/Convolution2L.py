# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Convolution2L(UGen):

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
        kernel=None,
        source=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel=kernel,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        crossfade=1,
        framesize=2048,
        kernel=None,
        source=None,
        trigger=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel=kernel,
            source=source,
            trigger=trigger,
            )
        return ugen
