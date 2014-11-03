# -*- encoding: utf-8 -*-
from supriya.tools.pendingugens.AbstractIn import AbstractIn


class LocalIn(AbstractIn):

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
        channel_count=1,
        default=0,
        ):
        AbstractIn.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        default=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        channel_count=1,
        default=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
            )
        return ugen
