# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BindingSource(SupriyaObject):

    ### INITIALIZER ###

    def __init__(self):
        self._binding_targets = set()

    ### PUBLIC METHODS ###

    def unbind(self, binding=None):
        if binding is None:
            for binding in self._binding_targets:
                binding.unbind()
        elif self is binding.source:
            binding.unbind()