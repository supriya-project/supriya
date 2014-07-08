# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class CSetnResponse(SupriyaValueObject, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        ):
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items