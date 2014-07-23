# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferSetContiguousRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_index_values_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        index_values_pairs=None,
        ):
        self._buffer_id = buffer_id
        if index_values_pairs:
            pairs = []
            for index, values in index_values_pairs:
                index = int(index)
                values = tuple(float(value) for value in values)
                pair = (index, values)
                pairs.append(pair)
            pairs = tuple(pairs)
        self._index_values_pairs = pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        if self.index_values_pairs:
            for index, values in self.index_values_pairs:
                if not values:
                    continue
                contents.append(index)
                contents.append(len(values))
                for value in values:
                    contents.append(value)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_values_pairs(self):
        return self._index_values_pairs

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_SET_CONTIGUOUS