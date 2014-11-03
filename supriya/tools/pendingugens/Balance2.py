# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Balance2(MultiOutUGen):

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
        left=None,
        level=1,
        pos=0,
        right=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            left=left,
            level=level,
            pos=pos,
            right=right,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        left=None,
        level=1,
        pos=0,
        right=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            left=left,
            level=level,
            pos=pos,
            right=right,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        left=None,
        level=1,
        pos=0,
        right=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            left=left,
            level=level,
            pos=pos,
            right=right,
            )
        return ugen
