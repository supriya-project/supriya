# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SendTrig(UGen):

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
        id=0,
        source=0,
        value=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        id=0,
        source=0,
        value=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        id=0,
        source=0,
        value=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )
        return ugen
