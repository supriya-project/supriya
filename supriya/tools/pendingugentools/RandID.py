# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class RandID(WidthFirstUGen):

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
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            id=id,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        id=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        id=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            )
        return ugen
