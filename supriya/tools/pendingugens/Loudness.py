# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Loudness(UGen):

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
        smask=0.25,
        tmask=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chain=chain,
            smask=smask,
            tmask=tmask,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        chain=None,
        smask=0.25,
        tmask=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chain=chain,
            smask=smask,
            tmask=tmask,
            )
        return ugen
