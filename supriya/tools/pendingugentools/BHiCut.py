# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.BEQSuite import BEQSuite


class BHiCut(BEQSuite):

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
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )

    ### PUBLIC METHODS ###

    # def allRQs(): ...

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

    # def coeffs(): ...

    # def filterClass(): ...

    # def initClass(): ...

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

    # def new1(): ...

    # def newFixed(): ...

    # def newVari(): ...
