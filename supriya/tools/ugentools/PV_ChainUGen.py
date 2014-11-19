# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class PV_ChainUGen(WidthFirstUGen):
    r'''Abstract base class of all phase-vocoder-chain unit generators.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'FFT UGens'

    __slots__ = ()