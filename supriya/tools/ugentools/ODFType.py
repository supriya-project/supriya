# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class ODFType(Enumeration):
    r'''ODFType enumeration, used by Onsets.
    '''

    ### CLASS VARIABLES ###

    POWER = 0
    MAGSUM = 1
    COMPLEX = 2
    RCOMPLEX = 3
    PHASE = 4
    WPHASE = 5
    MKL = 6