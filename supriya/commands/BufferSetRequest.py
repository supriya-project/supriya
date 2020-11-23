import supriya.osc
from .bases import Request
from supriya.enums import RequestId


class BufferSetRequest(Request):
    """
    A /b_set request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferSetRequest(
        ...     buffer_id=23,
        ...     index_value_pairs=(
        ...         (0, 1.0),
        ...         (10, 13.2),
        ...         (17, 19.3),
        ...         ),
        ...     )
        >>> request
        BufferSetRequest(
            buffer_id=23,
            index_value_pairs=(
                (0, 1.0),
                (10, 13.2),
                (17, 19.3),
                ),
            )

    ::

        >>> request.to_osc()
        OscMessage('/b_set', 23, 0, 1.0, 10, 13.2, 17, 19.3)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_SET

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_value_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if index_value_pairs:
            pairs = []
            for index, value in index_value_pairs:
                index = int(index)
                value = float(value)
                pair = (index, value)
                pairs.append(pair)
            pairs = tuple(pairs)
        self._index_value_pairs = index_value_pairs

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.index_value_pairs:
            for index, value in self.index_value_pairs:
                contents.append(index)
                contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_value_pairs(self):
        return self._index_value_pairs
