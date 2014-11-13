# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class UGenArray(UGenMethodMixin, collections.Sequence):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = (
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(self, ugens):
        assert isinstance(ugens, collections.Iterable)
        ugens = tuple(ugens)
        assert len(ugens)
        self._ugens = ugens

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self.ugens[i]

    def __len__(self):
        return len(self.ugens)

    def __repr__(self):
        return '{}({{{}}})'.format(
            type(self).__name__,
            len(self),
            )

    ### PUBLIC METHODS ###

    def scale(
        self,
        input_minimum,
        input_maximum,
        output_minimum,
        output_maximum,
        ):
        ugens = []
        for ugen in self:
            ugen = ugen.scale(
                input_minimum=input_minimum,
                input_maximum=input_maximum,
                output_minimum=output_minimum,
                output_maximum=output_maximum,
                )
            ugens.append(ugen)
        return type(self)(ugens)

    ### PUBLIC PROPERTIES ###

    @property
    def ugens(self):
        return self._ugens