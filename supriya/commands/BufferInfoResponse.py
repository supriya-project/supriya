from typing import NamedTuple

from .bases import Response


class BufferInfoResponse(Response):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        buffer_id: int
        frame_count: int
        channel_count: int
        sample_rate: int

    ### INITIALIZER ###

    def __init__(self, items=None):
        self._items = tuple(items or ())

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response(s) from OSC message.

        ::

            >>> message = supriya.osc.OscMessage('/b_info', 1100, 512, 1, 44100.0)
            >>> supriya.commands.BufferInfoResponse.from_osc_message(message)
            BufferInfoResponse(
                items=(
                    Item(buffer_id=1100, frame_count=512, channel_count=1, sample_rate=44100.0),
                    ),
                )

        """
        # TODO: Return one single thing
        items = []
        for group in cls._group_items(osc_message.contents, 4):
            item = cls.Item(*group)
            items.append(item)
        return cls(items=items)

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self[0].buffer_id

    @property
    def items(self):
        return self._items
