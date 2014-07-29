# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NotifyRequest(Request):
    r'''A /notify message.

    ::

        >>> from supriya.tools import requesttools

        >>> request = requesttools.NotifyRequest(
        ...     notify_status=True,
        ...     )
        >>> request
        NotifyRequest(
            notify_status=True
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(1, 1)

    ::

        >>> message.address == requesttools.RequestId.NOTIFY
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_notify_status',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        notify_status=None,
        ):
        Request.__init__(self)
        self._notify_status = bool(notify_status)

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        notify_status = int(self.notify_status)
        message = osctools.OscMessage(
            request_id,
            notify_status,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def notify_status(self):
        return self._notify_status

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.DoneResponse: {
                'action': ('/notify', 0),
                },
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.NOTIFY