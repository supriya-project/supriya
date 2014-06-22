# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class ControlDur(InfoUGenBase):
    r'''Control duration info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.ControlDur.ir()
        ControlDur.ir()

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
