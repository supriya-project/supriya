import collections
from typing import NamedTuple

from supriya.commands.Response import Response


class ControlBusSetResponse(Response, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = ("_items",)

    class Item(NamedTuple):
        bus_id: int
        bus_value: float

    ### INITIALIZER ###

    def __init__(self, items=None, osc_message=None):
        Response.__init__(self, osc_message=osc_message)
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        items = []
        for group in cls._group_items(osc_message.contents, 2):
            item = cls.Item(*group)
            items.append(item)
        response = cls(items=tuple(items))
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items
