# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufDur(BufInfoUGenBase):
    r'''Buffer duration info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufDur.kr(buffer_number=0)
        BufDur.kr()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_number=None,
        rate=None,
        ):
        BufInfoUGenBase.__init__(
            self,
            buffer_number=buffer_number,
            rate=rate,
            )
