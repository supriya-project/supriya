import supriya.osc
from supriya.commands.Request import Request
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

        >>> message = request.to_osc()
        >>> message
        OscMessage(1, 1)

    ::

        >>> message.address == supriya.RequestId.NOTIFY
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_notify_status",)

    request_id = RequestId.NOTIFY

    ### INITIALIZER ###

    def __init__(self, notify_status=None):
        Request.__init__(self)
        self._notify_status = bool(notify_status)

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
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
