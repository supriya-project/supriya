# -*- encoding: utf-8 -*-
from supriya.tools.serverresponsetools.ServerResponse import ServerResponse


class BufferSetContiguousResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_number',
        '_items',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        buffer_number=None
        ):
        self._buffer_number = buffer_number
        self._items = items

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_number(self):
        return self._buffer_number

    @property
    def items(self):
        return self._items
