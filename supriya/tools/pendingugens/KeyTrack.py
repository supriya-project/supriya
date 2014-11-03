# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class KeyTrack(UGen):

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
        chromaleak=0.5,
        keydecay=2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chain=chain,
            chromaleak=chromaleak,
            keydecay=keydecay,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        chain=None,
        chromaleak=0.5,
        keydecay=2,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chain=chain,
            chromaleak=chromaleak,
            keydecay=keydecay,
            )
        return ugen
