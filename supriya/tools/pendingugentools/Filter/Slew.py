# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Slew(Filter):

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
        dn=1,
        source=0,
        up=1,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            dn=dn,
            source=source,
            up=up,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        dn=1,
        source=0,
        up=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            dn=dn,
            source=source,
            up=up,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        dn=1,
        source=0,
        up=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            dn=dn,
            source=source,
            up=up,
            )
        return ugen
