import collections
from supriya.synthdefs.UGenMethodMixin import UGenMethodMixin


class UGenArray(UGenMethodMixin, collections.Sequence):

    ### CLASS VARIABLES ###

    __documentation_section__ = "SynthDef Internals"

    __slots__ = ("_ugens",)

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
        return "{}({{{}}})".format(type(self).__name__, len(self))

    ### PUBLIC PROPERTIES ###

    @property
    def ugens(self):
        return self._ugens
