# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        source=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            source=source,
            special_index=special_index,
            )