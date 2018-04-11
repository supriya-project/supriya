from supriya.tools.systemtools.Enumeration import Enumeration


class ParameterRate(Enumeration):
    """
    An enumeration of synthdef control rates.
    """

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 3
    SCALAR = 0
    TRIGGER = 1
