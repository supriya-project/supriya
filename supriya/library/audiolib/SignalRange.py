# -*- encoding: utf-8 -*-
from supriya.library.systemlib.Enumeration import Enumeration


class SignalRange(Enumeration):
    r'''An enumeration of scsynth UGen signal ranges.

    ::

        >>> from supriya.library import audiolib
        >>> audiolib.SignalRange.UNIPOLAR
        <SignalRange.UNIPOLAR: 0>

    ::

        >>> audiolib.SignalRange.from_expr('bipolar')
        <SignalRange.BIPOLAR: 1>

    '''

    ### CLASS VARIABLES ###

    UNIPOLAR = 0
    BIPOLAR = 1
