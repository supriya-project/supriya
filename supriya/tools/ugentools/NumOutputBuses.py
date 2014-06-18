# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class NumOutputBuses(InfoUGenBase):
    r'''Number of output buses info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.NumOutputBuses.ir()
        NumOutputBuses.ir()

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
