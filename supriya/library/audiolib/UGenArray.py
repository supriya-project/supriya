import collections


class UGenArray(collections.Sequence):

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

    def __add__(self, expr):
        return type(self)([x + expr for x in self.ugens])

    def __div__(self, expr):
        return type(self)([x / expr for x in self.ugens])

    def __getitem__(self, i):
        return self.ugens[i]

    def __len__(self):
        return len(self.ugens)

    def __mod__(self, expr):
        return type(self)([x % expr for x in self.ugens])

    def __mul__(self, expr):
        return type(self)([x * expr for x in self.ugens])

    def __neg__(self):
        return type(self)([-x for x in self.ugens])

    def __radd__(self, expr):
        return self.__add__(expr)

    def __rdiv__(self, expr):
        return self.__div__(expr)

    def __rmul__(self, expr):
        return self.__mul__(expr)

    def __rsub__(self, expr):
        return self.__sub__(expr)

    def __sub__(self, expr):
        return type(self)([x - expr for x in self.ugens])

    ### PUBLIC PROPERTIES ###

    @property
    def ugens(self):
        return self._ugens
