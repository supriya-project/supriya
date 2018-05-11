from uqbar.enums import IntEnumeration


class ODFType(IntEnumeration):
    """
    ODFType enumeration, used by Onsets.
    """

    ### CLASS VARIABLES ###

    POWER = 0
    MAGSUM = 1
    COMPLEX = 2
    RCOMPLEX = 3
    PHASE = 4
    WPHASE = 5
    MKL = 6
