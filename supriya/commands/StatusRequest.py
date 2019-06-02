import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class StatusRequest(Request):
    """
    A /status request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.StatusRequest()
        >>> request
        StatusRequest()

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(2)

    ::

        >>> message.address == supriya.RequestId.STATUS
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.STATUS

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        message = supriya.osc.OscMessage(request_id)
        return message
