# -*- encoding: utf-8 -*-
import enum
from supriya.tools.synthesistools.Argument import Argument
from supriya.tools.synthesistools.UGen import UGen


class BinaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _argument_specifications = (
        Argument('left'),
        Argument('right'),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left=None,
        right=None,
        calculation_rate=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            left=left,
            right=right,
            special_index=special_index,
            )
