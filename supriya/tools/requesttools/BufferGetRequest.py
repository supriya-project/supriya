# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferGetRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_indices',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        indices=None,
        ):
        self._buffer_id = buffer_id
        self._indices = tuple(int(index) for index in indices)

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        if self.indices:
            for index in self.indices:
                contents.append(index)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def indices(self):
        return self._indices

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_GET