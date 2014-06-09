# -*- encoding: utf-8 -*-
from supriya.tools.systemlib.Enumeration import Enumeration


class SignalRange(Enumeration):
    r'''An enumeration of scsynth UGen signal ranges.

    ::

        >>> from supriya.tools import audiotools
        >>> audiotools.SignalRange.UNIPOLAR
        <SignalRange.UNIPOLAR: 0>

    ::

        >>> audiotools.SignalRange.from_expr('bipolar')
        <SignalRange.BIPOLAR: 1>

    '''

    ### CLASS VARIABLES ###

    UNIPOLAR = 0
    BIPOLAR = 1
