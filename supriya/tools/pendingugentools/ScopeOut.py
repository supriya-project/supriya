# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class ScopeOut(UGen):

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
        input_array=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            input_array=input_array,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufnum=0,
        input_array=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            input_array=input_array,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bufnum=0,
        input_array=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            input_array=input_array,
            )
        return ugen
