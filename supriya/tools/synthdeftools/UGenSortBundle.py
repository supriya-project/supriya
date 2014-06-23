# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenSortBundle(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_antecedents',
        '_descendants',
        '_ugen',
        '_width_first_antecedents',
        )

    ### INITIALIZER ###

    def __init__(self, ugen):
        self._antecedents = []
        self._descendants = []
        self._ugen = ugen
        self._width_first_antecedents = []

    ### PRIVATE METHODS ###

    def _initialize_topological_sort(self, sort_bundles):
        from supriya import synthdeftools
        for input_ in self.ugen.inputs:
            if isinstance(input_, synthdeftools.OutputProxy):
                ugen = input_.source
                ugen_sort_bundle = sort_bundles[ugen]
                if ugen not in self.antecedents:
                    self.antecedents.append(ugen)
                if self.ugen not in ugen_sort_bundle.descendants:
                    ugen_sort_bundle.descendants.append(self.ugen)
        for ugen in self.width_first_antecedents:
            ugen_sort_bundle = sort_bundles[ugen]
            if ugen not in self.antecedents:
                self.antecedents.append(ugen)
            if self.ugen not in ugen_sort_bundle.descendants:
                ugen_sort_bundle.descendants.append(self)

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
