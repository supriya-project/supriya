# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class NumInputBuses(InfoUGenBase):
    r'''Number of input busses info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.NumInputBuses.ir()
        NumInputBuses.ir()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ):
        InfoUGenBase.__init__(
            self,
            calculation_rate=calculation_rate,
            )
