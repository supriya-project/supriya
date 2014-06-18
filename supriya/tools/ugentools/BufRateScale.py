# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufRateScale(BufInfoUGenBase):
    r'''Buffer sample rate scale info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufRateScale.kr(buffer_number=0)
        BufRateScale.kr()

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
