# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenSortBundle(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = (
        '_antecedents',
        '_descendants',
        '_ugen',
        '_width_first_antecedents',
        )

    ### INITIALIZER ###

    def __init__(self, ugen, width_first_antecedents):
        self._antecedents = []
        self._descendants = []
        self._ugen = ugen
        self._width_first_antecedents = tuple(width_first_antecedents)

    ### PRIVATE METHODS ###

    def _initialize_topological_sort(self, sort_bundles):
        from supriya import synthdeftools
        for input_ in self.ugen.inputs:
            if isinstance(input_, synthdeftools.OutputProxy):
                input_ = input_.source
            elif not isinstance(input_, synthdeftools.UGen):
                continue
            input_sort_bundle = sort_bundles[input_]
            if input_ not in self.antecedents:
                self.antecedents.append(input_)
            if self.ugen not in input_sort_bundle.descendants:
                input_sort_bundle.descendants.append(self.ugen)
        for input_ in self.width_first_antecedents:
            input_sort_bundle = sort_bundles[input_]
            if input_ not in self.antecedents:
                self.antecedents.append(input_)
            if self.ugen not in input_sort_bundle.descendants:
                input_sort_bundle.descendants.append(self.ugen)

    def _make_available(self, available_ugens):
        if not self.antecedents:
            if self.ugen not in available_ugens:
                available_ugens.append(self.ugen)

    def _schedule(self, available_ugens, out_stack, sort_bundles):
        for ugen in reversed(self.descendants):
            sort_bundle = sort_bundles[ugen]
            sort_bundle.antecedents.remove(self.ugen)
            sort_bundle._make_available(available_ugens)
        out_stack.append(self.ugen)

    ### PUBLIC METHODS ###

    def clear(self):
        self.antecedents[:] = []
        self.descendants[:] = []
        self.width_first_antecedents[:] = []

    ### PUBLIC PROPERTIES ###

    @property
    def antecedents(self):
        return self._antecedents

    @property
    def descendants(self):
        return self._descendants

    @property
    def ugen(self):
        return self._ugen

    @property
    def width_first_antecedents(self):
        return self._width_first_antecedents