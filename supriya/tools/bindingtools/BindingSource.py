# -*- encoding: utf-8 -*-
import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BindingSource(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, output_range=None):
        from supriya.tools import synthdeftools
        self._binding_targets = set()
        if output_range is not None:
            output_range = synthdeftools.Range(output_range)
        else:
            output_range = synthdeftools.Range(0, 1)
        self._output_range = output_range

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