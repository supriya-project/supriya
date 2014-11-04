# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PartConv(UGen):

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
        fftsize=None,
        irbufnum=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            fftsize=fftsize,
            irbufnum=irbufnum,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        fftsize=None,
        irbufnum=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            fftsize=fftsize,
            irbufnum=irbufnum,
            source=source,
            )
        return ugen

    # def calcBufSize(): ...

    # def calcNumPartitions(): ...
