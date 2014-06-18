# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufFrames(BufInfoUGenBase):
    r'''Buffer frame count info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufFrames.kr(buffer_number=0)
        BufFrames.kr()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_number=None,
        calculation_rate=None,
        ):
        BufInfoUGenBase.__init__(
            self,
            buffer_number=buffer_number,
            calculation_rate=calculation_rate,
            )
