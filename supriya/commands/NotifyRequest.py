import supriya.osc
from .bases import Request
from supriya.enums import RequestId


class NotifyRequest(Request):
    """
    A /notify message.

    ::

        >>> import supriya.commands

        >>> request = supriya.commands.NotifyRequest(
        ...     notify_status=True,
        ...     )
        >>> request
        NotifyRequest(
            notify_status=True,
            )

    ::

        >>> request.to_osc()
        OscMessage('/notify', 1)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NOTIFY

    ### INITIALIZER ###

    def __init__(self, notify_status=None):
        Request.__init__(self)
        self._notify_status = bool(notify_status)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        notify_status = int(self.notify_status)
        message = supriya.osc.OscMessage(request_id, notify_status)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def notify_status(self):
        return self._notify_status

    @property
    def response_patterns(self):
        return ["/done", "/notify"], ["/fail", "/notify"]
