# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BindingTarget(SupriyaObject):

    ### INITIALIZER ###

    def __init__(self):
        self._binding_sources = set()

    ### PRIVATE METHODS ###

    def _receive_bound_event(self, event=None):
        print('Received {!r} @ {}'.format(event, self))

    ### PUBLIC METHODS ###

    def unbind(self, binding=None):
        if binding is None:
            for binding in self._binding_sources:
                binding.unbind()
        elif self is binding.target:
            binding.unbind()