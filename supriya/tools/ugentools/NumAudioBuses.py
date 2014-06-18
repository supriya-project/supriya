# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class NumAudioBuses(InfoUGenBase):
    r'''Number of audio busses info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.NumAudioBuses.ir()
        NumAudioBuses.ir()

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
