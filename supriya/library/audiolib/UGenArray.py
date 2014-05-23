import collections
import operator


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
        return self._operate(expr, operator.add)

    def __div__(self, expr):
        return self._operate(expr, operator.div)

    def __getitem__(self, i):
        return self.ugens[i]

    def __len__(self):
        return len(self.ugens)

    def __mod__(self, expr):
        return self._operate(expr, operator.mod)

    def __mul__(self, expr):
        return self._operate(expr, operator.mul)

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
        return self._operate(expr, operator.sub)

    ### PRIVATE METHODS ###

    def _operate(self, expr, operator):
        from supriya.library import audiolib
        result = []
        if isinstance(expr, collections.Sequence):
            sequences = (self, expr)
            max_length = max(len(x) for x in sequences)
            for i in range(max_length):
                part = []
                for sequence in sequences:
                    index = i % len(sequence)
                    part.append(sequence[index])
                subresult = operator(part[0], part[1])
                if isinstance(subresult, audiolib.UGen):
                    result.append(subresult)
                else:
                    result.extend(subresult)
        else:
            for x in self.ugens:
                result.extend(operator(x, expr))
        prototype = (audiolib.OutputProxy, audiolib.UGen)
        assert all(isinstance(x, prototype) for x in result), result
        return type(self)(result)

    ### PUBLIC PROPERTIES ###

    @property
    def ugens(self):
        return self._ugens
