# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.K2A import K2A


class T2A(K2A):

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
        offset=0,
        source=0,
        ):
        K2A.__init__(
            self,
            calculation_rate=calculation_rate,
            offset=offset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        offset=0,
        source=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            offset=offset,
            source=source,
            )
        return ugen
