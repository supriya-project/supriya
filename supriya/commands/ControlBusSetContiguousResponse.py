import collections
from typing import NamedTuple, Tuple

from supriya.commands.Response import Response


class ControlBusSetContiguousResponse(Response, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = ('_items',)

    class Item(NamedTuple):
        bus_values: Tuple[float]
        starting_bus_id: int

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
        contents = list(osc_message.contents)
        while contents:
            starting_bus_id = contents[0]
            bus_count = contents[1]
            bus_values = tuple(contents[2 : 2 + bus_count])
            item = cls.Item(starting_bus_id=starting_bus_id, bus_values=bus_values)
            items.append(item)
            contents = contents[2 + bus_count :]
        items = tuple(items)
        response = cls(items=items)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items
