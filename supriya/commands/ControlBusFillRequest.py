import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class ControlBusFillRequest(Request):
    """
    A /c_fill request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.ControlBusFillRequest(
        ...     index_count_value_triples=[
        ...         (0, 8, 0.5),
        ...         (8, 8, 0.25),
        ...         ],
        ...     )
        >>> request
        ControlBusFillRequest(
            index_count_value_triples=(
                (0, 8, 0.5),
                (8, 8, 0.25),
                ),
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(27, 0, 8, 0.5, 8, 8, 0.25)

    ::

        >>> message.address == supriya.commands.RequestId.CONTROL_BUS_FILL
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_index_count_value_triples",)

    request_id = RequestId.CONTROL_BUS_FILL

    ### INITIALIZER ###

    def __init__(self, index_count_value_triples=None):
        Request.__init__(self)
        if index_count_value_triples:
            triples = []
            for index, count, value in index_count_value_triples:
                index = int(index)
                count = int(count)
                value = float(value)
                assert 0 <= index
                assert 0 < count
                triple = (index, count, value)
                triples.append(triple)
            index_count_value_triples = tuple(triples)
        self._index_count_value_triples = index_count_value_triples

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.index_count_value_triples:
            for index, count, value in self.index_count_value_triples:
                contents.append(index)
                contents.append(count)
                contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_count_value_triples(self):
        return self._index_count_value_triples
