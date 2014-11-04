# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SelectL(UGen):

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
        array=None,
        which=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        array=None,
        which=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )
        return ugen

    # def arSwitch(): ...

    @classmethod
    def kr(
        cls,
        array=None,
        which=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )
        return ugen
