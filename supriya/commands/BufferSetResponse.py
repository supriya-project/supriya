import collections
from typing import NamedTuple

from .bases import Response


class BufferSetResponse(Response, collections.Sequence):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        sample_index: int
        sample_value: float

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, items=None):
        self._buffer_id = buffer_id
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    def as_dict(self):
        result = collections.OrderedDict()
        for item in self:
            result[item.sample_index] = item.sample_value
        return result

    @classmethod
    def from_osc_message(cls, osc_message):
        buffer_id, remainder = osc_message.contents[0], osc_message.contents[1:]
        items = []
        for group in cls._group_items(remainder, 2):
            item = cls.Item(*group)
            items.append(item)
        items = tuple(items)
        response = cls(buffer_id=buffer_id, items=items)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def items(self):
        return self._items
