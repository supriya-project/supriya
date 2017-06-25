import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Frame(SupriyaObject, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_values',
        )

    ### INITIALIZER ###

    def __init__(self, *values):
        assert len(values)
        values = tuple(float(x) for x in values)
        self._values = values

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._values[item]

    def __len__(self):
        return len(self._values)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return len(self)
