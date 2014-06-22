# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class BlockSize(InfoUGenBase):
    r'''Block size info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.BlockSize.ir()
        BlockSize.ir()

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
