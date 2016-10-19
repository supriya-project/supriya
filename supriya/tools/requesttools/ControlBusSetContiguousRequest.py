# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class ControlBusSetContiguousRequest(Request):
    r"""
    A /c_setn request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.ControlBusSetContiguousRequest(
        ...     index_values_pairs=[
        ...         (0, (0.1, 0.2, 0.3)),
        ...         (4, (0.4, 0.5, 0.6)),
        ...         ],
        ...     )
        >>> request
        ControlBusSetContiguousRequest(
            index_values_pairs=(
                (
                    0,
                    (0.1, 0.2, 0.3),
                    ),
                (
                    4,
                    (0.4, 0.5, 0.6),
                    ),
                )
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(26, 0, 3, 0.1, 0.2, 0.3, 4, 3, 0.4, 0.5, 0.6)

    ::

        >>> message.address == \
        ...     requesttools.RequestId.CONTROL_BUS_SET_CONTIGUOUS
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index_values_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        index_values_pairs=None,
        ):
        Request.__init__(self)
        if index_values_pairs:
            pairs = []
            for index, values in index_values_pairs:
                index = int(index)
                values = tuple(float(value) for value in values)
                assert 0 <= index
                assert values
                if not values:
                    continue
                pair = (index, values)
                pairs.append(pair)
            index_values_pairs = tuple(pairs)
        self._index_values_pairs = index_values_pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.index_values_pairs:
            for index, values in self.index_values_pairs:
                contents.append(index)
                contents.append(len(values))
                contents.extend(values)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_values_pairs(self):
        return self._index_values_pairs

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.CONTROL_BUS_SET_CONTIGUOUS
