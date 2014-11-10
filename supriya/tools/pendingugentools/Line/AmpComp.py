# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class AmpComp(PureUGen):

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
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        exp=0.3333,
        frequency=None,
        root=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            exp=exp,
            frequency=frequency,
            root=root,
            )
        return ugen
