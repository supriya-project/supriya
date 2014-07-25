# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class ControlBusGetRequest(Request):
    r'''A /c_get request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.ControlBusGetRequest(
        ...     indices=(0, 4, 8, 12),
        ...     )
        >>> request
        ControlBusGetRequest(
            indices=(0, 4, 8, 12)
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(40, 0, 4, 8, 12)

    ::

        >>> message.address == \
        ...     requesttools.RequestId.CONTROL_BUS_GET
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_indices',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        indices=None,
        ):
        if indices:
            indices = tuple(int(index) for index in indices)
            assert all(0 <= index for index in indices)
        self._indices = indices

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        contents = [request_id]
        if self.indices:
            contents.extend(self.indices)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        return self._indices

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.CONTROL_BUS_GET