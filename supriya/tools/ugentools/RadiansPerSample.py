# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.InfoUGenBase import InfoUGenBase


class RadiansPerSample(InfoUGenBase):
    r'''Radians-per-sample info unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.RadiansPerSample.ir()
        RadiansPerSample.ir()

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
