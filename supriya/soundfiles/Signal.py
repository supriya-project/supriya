from supriya.system.SupriyaObject import SupriyaObject


class Signal(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ("_values",)

    ### INITIALIZER ###

    def __init__(self, *values):
        values = tuple(float(x) for x in values)
        self._values = values

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._values[item]

    def __len__(self):
        return len(self._values)
