# -*- encoding: utf-8 -*-
from supriya.tools.bindingtools.BindingTarget import BindingTarget


class BindingOutput(BindingTarget):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_binding_sources',
        )

    ### INITIALIZER ###

    def __init__(self):
        BindingTarget.__init__(self)
