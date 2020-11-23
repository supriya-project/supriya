import supriya.osc
from supriya.enums import RequestId

from .bases import Request


class BufferQueryRequest(Request):
    """
    A /b_query request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferQueryRequest(
        ...     buffer_ids=(1, 23, 41)
        ...     )
        >>> request
        BufferQueryRequest(
            buffer_ids=(1, 23, 41),
            )

    ::

        >>> request.to_osc()
        OscMessage('/b_query', 1, 23, 41)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.BUFFER_QUERY

    ### INITIALIZER ###

    def __init__(self, buffer_ids=None):
        Request.__init__(self)
        if buffer_ids:
            buffer_ids = tuple(int(buffer_id) for buffer_id in buffer_ids)
        self._buffer_ids = buffer_ids

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        for buffer_id in self.buffer_ids:
            contents.append(buffer_id)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_ids(self):
        return self._buffer_ids

    @property
    def response_patterns(self):
        if 1 == len(self.buffer_ids):
            return ["/b_info", self.buffer_ids[0]], None
        return None, None
