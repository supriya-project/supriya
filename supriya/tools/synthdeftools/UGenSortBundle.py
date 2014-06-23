# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class UGenSortBundle(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_antecedents',
        '_descendants',
        '_synthdef',
        '_ugen',
        '_width_first_antecedents',
        )

    ### INITIALIZER ###

    def __init__(self, ugen):
        self._antecedents = []
        self._descendants = []
        self._synthdef = None
        self._ugen = ugen
        self._width_first_antecedents = []

    ### PRIVATE METHODS ###

    def _make_available(self):
        if not self.antecedents:
            if self.ugen not in self.synthdef._available_ugens:
                self.synthdef._available_ugens.append(self.ugen)

    def _schedule(self, out_stack):
        for ugen in reversed(self.descendants):
            ugen.sort_bundle.antecedents.remove(self.ugen)
            ugen.sort_bundle._make_available()
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
    def synthdef(self):
        return self._synthdef

    @synthdef.setter
    def synthdef(self, synthdef):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDef)
        self._synthdef = synthdef

    @property
    def ugen(self):
        return self._ugen

    @property
    def width_first_antecedents(self):
        return self._width_first_antecedents
