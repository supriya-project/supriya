# -*- encoding: utf-8 -*-
from supriya.tools.synthesistools.Argument import Argument
from supriya.tools.synthesistools.UGen import UGen


class Dust(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _argument_specifications = (
        Argument('density', 0.),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        density=0.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            density=density,
            )
