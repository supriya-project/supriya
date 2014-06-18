# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class SampleDur(InfoUGenBase):
    r'''Sample duration info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.SampleDur.ir()
        SampleDur.ir()

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
