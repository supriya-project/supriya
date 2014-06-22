# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class NumBuffers(InfoUGenBase):
    r'''Number of buffers info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.NumBuffers.ir()
        NumBuffers.ir()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            rate=rate,
            )
