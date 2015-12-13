# -*- encoding: utf-8 -*-
from supriya.tools.nrttools.NRTGroupProxy import NRTGroupProxy


class NRTRootProxy(NRTGroupProxy):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_nrt_time_slice',
        )

    ### INITIALIZER ###

    def __init__(self, nrt_time_slice, children=None):
        from supriya.tools import nrttools
        NRTGroupProxy.__init__(self, children=children)
        assert isinstance(nrt_time_slice, nrttools.NRTTimeSlice)
        self._nrt_time_slice = nrt_time_slice
