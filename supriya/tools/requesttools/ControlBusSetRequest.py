import supriya.osc
from supriya.tools.requesttools.Request import Request


class ControlBusSetRequest(Request):
    """
    A /c_set request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.ControlBusSetRequest(
        ...     index_value_pairs=[
        ...         (0, 0.1),
        ...         (1, 0.2),
        ...         (1, 0.3),
        ...         (1, 0.4),
        ...         ],
        ...     )
        >>> request
        ControlBusSetRequest(
            index_value_pairs=(
                (0, 0.1),
                (1, 0.2),
                (1, 0.3),
                (1, 0.4),
                ),
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(25, 0, 0.1, 1, 0.2, 1, 0.3, 1, 0.4)

    ::

        >>> message.address == requesttools.RequestId.CONTROL_BUS_SET
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index_value_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        index_value_pairs=None,
        ):
        Request.__init__(self)
        if index_value_pairs:
            pairs = []
            for index, value in index_value_pairs:
                index = int(index)
                value = float(value)
                assert 0 <= index
                pair = (index, value)
                pairs.append(pair)
            index_value_pairs = tuple(pairs)
        self._index_value_pairs = index_value_pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.index_value_pairs:
            for pair in self.index_value_pairs:
                contents.extend(pair)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_value_pairs(self):
        return self._index_value_pairs

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.CONTROL_BUS_SET
