# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class UGenArray(UGenMethodMixin, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(self, ugens):
        assert isinstance(ugens, collections.Sequence)
        assert len(ugens)
        self._ugens = tuple(ugens)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self.ugens[i]

    def __len__(self):
        return len(self.ugens)

    ### PUBLIC PROPERTIES ###

    @property
    def ugens(self):
        return self._ugens
