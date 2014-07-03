# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufRateScale(BufInfoUGenBase):
    r'''Buffer sample rate scale info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufRateScale.kr(buffer_id=0)
        BufRateScale.kr()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        rate=None,
        ):
        BufInfoUGenBase.__init__(
            self,
            buffer_id=buffer_id,
            rate=rate,
            )
