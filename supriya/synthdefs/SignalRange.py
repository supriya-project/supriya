from uqbar.enums import IntEnumeration


class SignalRange(IntEnumeration):
    """
    An enumeration of scsynth UGen signal ranges.

    ::

        >>> import supriya.synthdefs
        >>> supriya.synthdefs.SignalRange.UNIPOLAR
        SignalRange.UNIPOLAR

    ::

        >>> supriya.synthdefs.SignalRange.from_expr('bipolar')
        SignalRange.BIPOLAR

    """

    ### CLASS VARIABLES ###

    UNIPOLAR = 0
    BIPOLAR = 1
