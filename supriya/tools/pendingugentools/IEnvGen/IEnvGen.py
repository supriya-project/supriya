# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class IEnvGen(UGen):

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
        envelope=None,
        index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        envelope=None,
        index=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )
        return ugen

    # def convertEnv(): ...

    @classmethod
    def kr(
        cls,
        envelope=None,
        index=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            envelope=envelope,
            index=index,
            )
        return ugen

    # def new1(): ...
