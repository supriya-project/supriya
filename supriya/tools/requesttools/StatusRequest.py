# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class StatusRequest(Request):
    r'''A /status request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.StatusRequest()
        >>> request
        StatusRequest()

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(2)

    ::

        >>> message.address == requesttools.RequestId.STATUS
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        message = osctools.OscMessage(
            request_id,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.STATUS