import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class BufferGetContiguousRequest(Request):
    """
    A /b_getn request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferGetContiguousRequest(
        ...     buffer_id=23,
        ...     index_count_pairs=[(0, 3), (8, 11)],
        ...     )
        >>> request
        BufferGetContiguousRequest(
            buffer_id=23,
            index_count_pairs=(
                (0, 3),
                (8, 11),
                ),
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(43, 23, 0, 3, 8, 11)

    ::

        >>> message.address == supriya.RequestId.BUFFER_GET_CONTIGUOUS
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buffer_id", "_index_count_pairs")

    request_id = RequestId.BUFFER_GET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_count_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._index_count_pairs = tuple(
            (int(index), int(count)) for index, count in index_count_pairs
        )

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.index_count_pairs:
            for index, count in self.index_count_pairs:
                contents.append(index)
                contents.append(count)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_count_pairs(self):
        return self._index_count_pairs

    @property
    def response_patterns(self):
        return [["/b_setn", self.buffer_id], ["/fail", "/b_getn"]]
