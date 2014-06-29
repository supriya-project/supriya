# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Range(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_minimum',
        '_maximum',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        minimum=None,
        maximum=None,
        ):
        if minimum is None:
            minimum = float('-inf')
        minimum = float(minimum)
        if maximum is None:
            maximum = float('inf')
        maximum = float(maximum)
        assert minimum <= maximum
        self._minimum = minimum
        self._maximum = maximum
