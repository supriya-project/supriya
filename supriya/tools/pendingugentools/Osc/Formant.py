# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Formant(PureUGen):

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
        bwfrequency=880,
        formfrequency=1760,
        fundfrequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bwfrequency=bwfrequency,
            formfrequency=formfrequency,
            fundfrequency=fundfrequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bwfrequency=880,
        formfrequency=1760,
        fundfrequency=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bwfrequency=bwfrequency,
            formfrequency=formfrequency,
            fundfrequency=fundfrequency,
            )
        return ugen
