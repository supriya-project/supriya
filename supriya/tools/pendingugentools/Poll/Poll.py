# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Poll(UGen):

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
        label=None,
        source=None,
        trigger=None,
        trigid=-1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigid=trigid,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        label=None,
        source=None,
        trigger=None,
        trigid=-1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigid=trigid,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        label=None,
        source=None,
        trigger=None,
        trigid=-1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigid=trigid,
            )
        return ugen

    @classmethod
    def new(
        cls,
        label=None,
        source=None,
        trigger=None,
        trigid=-1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigid=trigid,
            )
        return ugen

    # def new1(): ...
