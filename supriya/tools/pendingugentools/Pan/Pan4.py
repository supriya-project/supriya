# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Pan4(MultiOutUGen):

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
        level=1,
        source=None,
        xpos=0,
        ypos=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            level=level,
            source=source,
            xpos=xpos,
            ypos=ypos,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        level=1,
        source=None,
        xpos=0,
        ypos=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            source=source,
            xpos=xpos,
            ypos=ypos,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        level=1,
        source=None,
        xpos=0,
        ypos=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            level=level,
            source=source,
            xpos=xpos,
            ypos=ypos,
            )
        return ugen
