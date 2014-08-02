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
        if not isinstance(minimum, (float, int)):
            raise ValueError(minimum)
        minimum = float(minimum)
        if maximum is None:
            maximum = float('inf')
        if not isinstance(maximum, (float, int)):
            raise ValueError(maximum)
        maximum = float(maximum)
        assert minimum <= maximum
        self._minimum = minimum
        self._maximum = maximum

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        return self._maximum

    @property
    def minimum(self):
        return self._minimum