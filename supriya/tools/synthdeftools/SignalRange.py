# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.Enumeration import Enumeration


class SignalRange(Enumeration):
    r"""
    An enumeration of scsynth UGen signal ranges.

    ::

        >>> from supriya.tools import synthdeftools
        >>> synthdeftools.SignalRange.UNIPOLAR
        SignalRange.UNIPOLAR

    ::

        >>> synthdeftools.SignalRange.from_expr('bipolar')
        SignalRange.BIPOLAR

    """

    ### CLASS VARIABLES ###

    UNIPOLAR = 0
    BIPOLAR = 1
