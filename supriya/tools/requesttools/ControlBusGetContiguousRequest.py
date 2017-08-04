from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class ControlBusGetContiguousRequest(Request):
    """
    A /c_getn request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.ControlBusGetContiguousRequest(
        ...     index_count_pairs=[
        ...         (0, 2),
        ...         (4, 2),
        ...         (8, 2),
        ...         (12, 2),
        ...         ],
        ...     )
        >>> request
        ControlBusGetContiguousRequest(
            index_count_pairs=(
                (0, 2),
                (4, 2),
                (8, 2),
                (12, 2),
                )
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(41, 0, 2, 4, 2, 8, 2, 12, 2)

    ::

        >>> message.address == requesttools.RequestId.CONTROL_BUS_GET_CONTIGUOUS
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index_count_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        index_count_pairs=None,
        ):
        Request.__init__(self)
        if index_count_pairs:
            pairs = []
            for index, count in index_count_pairs:
                index = int(index)
                count = int(count)
                assert 0 <= index
                assert 0 < count
                pair = (index, count)
                pairs.append(pair)
            index_count_pairs = tuple(pairs)
        self._index_count_pairs = index_count_pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.index_count_pairs:
            for pair in self.index_count_pairs:
                contents.extend(pair)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_count_pairs(self):
        return self._index_count_pairs

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.ControlBusSetContiguousResponse: None,
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.CONTROL_BUS_GET_CONTIGUOUS
