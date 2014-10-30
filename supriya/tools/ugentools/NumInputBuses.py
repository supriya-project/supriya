# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class NumInputBuses(InfoUGenBase):
    r'''Number of input buses info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.NumInputBuses.ir()
        NumInputBuses.ir()

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