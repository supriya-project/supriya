# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class BinaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _ordered_input_names = (
        'left',
        'right',
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
