# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufChannels(BufInfoUGenBase):
    r'''Buffer channel count info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufChannels.kr(buffer_id=0)
        BufChannels.kr()

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
