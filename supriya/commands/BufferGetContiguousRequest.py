import supriya.osc
from supriya.enums import RequestId

from .bases import Request


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

        >>> request.to_osc()
        OscMessage('/b_getn', 23, 0, 3, 8, 11)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_GET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_count_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        self._index_count_pairs = tuple(
            (int(index), int(count)) for index, count in index_count_pairs
        )

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
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
        return ["/b_setn", self.buffer_id], ["/fail", "/b_getn"]
