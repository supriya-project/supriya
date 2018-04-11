import supriya.osc
from supriya.tools.requesttools.Request import Request


class BufferFillRequest(Request):
    """
    A /b_fill request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.BufferFillRequest(
        ...     buffer_id=23,
        ...     index_count_value_triples=(
        ...         (0, 8, 0.1),
        ...         (11, 4, 0.2),
        ...         ),
        ...     )
        >>> request
        BufferFillRequest(
            buffer_id=23,
            index_count_value_triples=(
                (0, 8, 0.1),
                (11, 4, 0.2),
                ),
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(37, 23, 0, 8, 0.1, 11, 4, 0.2)

    ::

        >>> message.address == requesttools.RequestId.BUFFER_FILL
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_buffer_id',
        '_index_count_value_triples',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=None,
        index_count_value_triples=None,
        ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        triples = []
        for index, count, value in index_count_value_triples:
            triple = (int(index), int(count), float(value))
            triples.append(triple)
        triples = tuple(triples)
        self._index_count_value_triples = triples

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            ]
        for index, count, value in self.index_count_value_triples:
            contents.append(int(index))
            contents.append(int(count))
            contents.append(float(value))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_count_value_triples(self):
        return self._index_count_value_triples

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.BUFFER_FILL
