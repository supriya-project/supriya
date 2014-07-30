# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class BufferGetContiguousRequest(Request):
    r'''A /b_getn request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferGetContiguousRequest(
        ...     buffer_id=23,
        ...     index_count_pairs=[(0, 3), (8, 11)],
        ...     )
        >>> request
        BufferGetContiguousRequest(
            buffer_id=23,
            index_count_pairs=(
                (0, 3),
                (8, 11),
                )
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(43, 23, 0, 3, 8, 11)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_GET_CONTIGUOUS
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_index_count_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        index_count_pairs=None,
        ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._index_count_pairs = tuple(
            (int(index), int(count))
            for index, count in index_count_pairs
            )

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        if self.index_count_pairs:
            for index, count in self.index_count_pairs:
                contents.append(index)
                contents.append(count)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_count_pairs(self):
        return self._index_count_pairs

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.BufferSetContiguousResponse: {
                'buffer_id': self.buffer_id,
                }
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_GET_CONTIGUOUS