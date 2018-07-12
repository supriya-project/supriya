import collections
from typing import NamedTuple
from supriya.commands.Response import Response


class BufferSetContiguousResponse(Response, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_items',
        )

    class Item(NamedTuple):
        sample_values: int
        starting_sample_index: int

    ### INITIALIZER ###

    def __init__(self, items=None, buffer_id=None, osc_message=None):
        Response.__init__(self, osc_message=osc_message)
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
            result[item.starting_sample_index] = item.sample_values
        return result

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response from OSC message.

        ::

            >>> message = supriya.osc.OscMessage('/b_setn', 1, 0, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            >>> supriya.commands.BufferSetContiguousResponse.from_osc_message(message)
            BufferSetContiguousResponse(
                buffer_id=1,
                items=(
                    Item(sample_values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), starting_sample_index=0),
                    ),
                )

        """
        buffer_id, remainder = osc_message.contents[0], osc_message.contents[1:]
        items = []
        while remainder:
            starting_sample_index = remainder[0]
            sample_count = remainder[1]
            sample_values = tuple(remainder[2:2 + sample_count])
            item = cls.Item(
                starting_sample_index=starting_sample_index,
                sample_values=sample_values,
                )
            items.append(item)
            remainder = remainder[2 + sample_count:]
        items = tuple(items)
        response = cls(
            buffer_id=buffer_id,
            items=items,
            )
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def items(self):
        return self._items
