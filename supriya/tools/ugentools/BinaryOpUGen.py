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
        rate=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            left=left,
            right=right,
            special_index=special_index,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def left(self):
        index = self._ordered_input_names.index('left')
        return self._inputs[index]

    @property
    def right(self):
        index = self._ordered_input_names.index('right')
        return self._inputs[index]