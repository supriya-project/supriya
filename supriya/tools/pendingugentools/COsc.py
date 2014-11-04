# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class COsc(PureUGen):

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
        beats=0.5,
        bufnum=None,
        frequency=440,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            beats=beats,
            bufnum=bufnum,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        beats=0.5,
        bufnum=None,
        frequency=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            beats=beats,
            bufnum=bufnum,
            frequency=frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        beats=0.5,
        bufnum=None,
        frequency=440,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            beats=beats,
            bufnum=bufnum,
            frequency=frequency,
            )
        return ugen
