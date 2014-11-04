# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class MantissaMask(UGen):

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
        bits=3,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bits=bits,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bits=3,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bits=bits,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bits=3,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bits=bits,
            source=source,
            )
        return ugen
