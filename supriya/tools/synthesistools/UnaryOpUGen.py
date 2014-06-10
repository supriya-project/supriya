# -*- encoding: utf-8 -*-
from supriya.tools.synthesistools.Argument import Argument
from supriya.tools.synthesistools.UGen import UGen


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _argument_specifications = (
        Argument('source'),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            special_index=special_index,
            )
