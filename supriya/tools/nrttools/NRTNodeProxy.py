# -*- encoding: utf-8 -*-
from supriya.tools.datastructuretools.TreeNode import TreeNode
class NRTNodeProxy(TreeNode):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_parent',
        )

    ### INITIALIZER ###

    def __init__(self):
        TreeNode.__init__(self)
