# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class SubsampleOffset(InfoUGenBase):
    r'''Subsample-offset info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.SubsampleOffset.ir()
        SubsampleOffset.ir()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Info UGens'

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