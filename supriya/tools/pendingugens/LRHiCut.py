# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.BHiCut import BHiCut


class LRHiCut(BHiCut):

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
        frequency=None,
        max_order=5,
        order=2,
        source=None,
        ):
        BHiCut.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=None,
        max_order=5,
        order=2,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=None,
        max_order=5,
        order=2,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )
        return ugen

    # def magResponse(): ...
