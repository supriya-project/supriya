# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class ControlRate(InfoUGenBase):
    r'''Control rate info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.ControlRate.ir()
        ControlRate.ir()

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