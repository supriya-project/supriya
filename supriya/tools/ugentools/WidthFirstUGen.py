# -*- encoding: utf-8 -*-
import abc
from supriya.tools.synthdeftools.UGen import UGen


class WidthFirstUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        rate=None,
        special_index=0,
        **kwargs
        ):
        UGen.__init__(
            self,
            rate=rate,
            special_index=special_index,
            **kwargs
            )
