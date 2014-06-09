# -*- encoding: utf-8 -*-
from supriya.tools.systemlib.Enumeration import Enumeration


class SignalRange(Enumeration):
    r'''An enumeration of scsynth UGen signal ranges.

    ::

        >>> from supriya.tools import synthdefinitiontools
        >>> synthdefinitiontools.SignalRange.UNIPOLAR
        <SignalRange.UNIPOLAR: 0>

    ::

        >>> synthdefinitiontools.SignalRange.from_expr('bipolar')
        <SignalRange.BIPOLAR: 1>

    '''

    ### CLASS VARIABLES ###

    UNIPOLAR = 0
    BIPOLAR = 1
