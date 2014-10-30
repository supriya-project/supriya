# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BufInfoUGenBase import BufInfoUGenBase


class BufSamples(BufInfoUGenBase):
    r'''Buffer sample count info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BufSamples.kr(buffer_id=0)
        BufSamples.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

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