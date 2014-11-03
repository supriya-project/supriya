# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.BEQSuite import BEQSuite


class BBandPass(BEQSuite):

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
        bw=1,
        frequency=1200,
        source=None,
        ):
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            bw=bw,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bw=1,
        frequency=1200,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bw=bw,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    # def sc(): ...
