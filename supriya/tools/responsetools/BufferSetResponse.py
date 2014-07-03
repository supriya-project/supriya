# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class BufferSetResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_items',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        items=None,
        ):
        self._buffer_id = buffer_id
        self._items = items

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def items(self):
        return self._items
