import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class BufferSetContiguousRequest(Request):
    """
    A /b_setn request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferSetContiguousRequest(
        ...     buffer_id=23,
        ...     index_values_pairs=(
        ...         (0, (1, 2, 3)),
        ...         (10, (17.1, 18.2))
        ...         ),
        ...     )
        >>> request
        BufferSetContiguousRequest(
            buffer_id=23,
            index_values_pairs=(
                (0, (1.0, 2.0, 3.0)),
                (10, (17.1, 18.2)),
                ),
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(36, 23, 0, 3, 1.0, 2.0, 3.0, 10, 2, 17.1, 18.2)

    ::

        >>> message.address == supriya.RequestId.BUFFER_SET_CONTIGUOUS
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buffer_id", "_index_values_pairs")

    request_id = RequestId.BUFFER_SET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_values_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
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

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.index_values_pairs:
            for index, values in self.index_values_pairs:
                if not values:
                    continue
                contents.append(index)
                contents.append(len(values))
                for value in values:
                    contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_values_pairs(self):
        return self._index_values_pairs
