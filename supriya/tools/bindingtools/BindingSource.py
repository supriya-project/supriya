# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BindingSource(SupriyaObject):

    ### INITIALIZER ###

    def __init__(self):
        self._binding_targets = set()

    ### PRIVATE METHODS ###

    def _send_bound_event(self, event=None):
        for binding in self._binding_targets:
            binding(event)

    ### PUBLIC METHODS ###

    def unbind(self, binding=None):
        if binding is None:
            for binding in self._binding_targets:
                binding.unbind()
        elif self is binding.source:
            binding.unbind()