# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class VOsc3(PureUGen):

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
        bufpos=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufpos=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bufpos=None,
        freq_1=110,
        freq_2=220,
        freq_3=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufpos=bufpos,
            freq_1=freq_1,
            freq_2=freq_2,
            freq_3=freq_3,
            )
        return ugen
