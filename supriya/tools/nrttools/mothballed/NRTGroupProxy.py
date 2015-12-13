# -*- encoding: utf-8 -*-
from supriya.tools.datastructuretools.TreeContainer import TreeContainer
from supriya.tools.nrttools.NRTNodeProxy import NRTNodeProxy


class NRTGroupProxy(NRTNodeProxy, TreeContainer):

    ### CLASS VARIABLES ###
    
    __slots__ = (
        '_children',
        '_name',
        '_named_children',
        '_parent',
        )

    ### INITIALIZER ###

    def __init__(self, children=None):
        NRTNodeProxy.__init__(self)
        TreeContainer.__init__(self, children=children)
