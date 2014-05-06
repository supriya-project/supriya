import collections


class UGenArray(collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_ugen_specifications',
        )

    ### INITIALIZER ###

    def __init__(self, ugen_specifications):
        assert isinstance(ugen_specifications, collections.Sequence)
        assert len(ugen_specifications)
        self._ugen_specifications = tuple(ugen_specifications)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        return type(self)([x + expr for x in self._ugen_specifications])

    def __div__(self, expr):
        return type(self)([x / expr for x in self._ugen_specifications])

    def __getitem__(self, i):
        return self._ugen_specifications[i]

    def __len__(self):
        return len(self._ugen_specifications)

    def __mod__(self, expr):
        return type(self)([x % expr for x in self._ugen_specifications])

    def __mul__(self, expr):
        return type(self)([x * expr for x in self._ugen_specifications])

    def __neg__(self):
        return type(self)([-x for x in self._ugen_specifications])

    def __sub__(self, expr):
        return type(self)([x - expr for x in self._ugen_specifications])
