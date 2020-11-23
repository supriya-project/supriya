import supriya.osc
from .bases import Request
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

        >>> request.to_osc()
        OscMessage('/status')

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.STATUS

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        message = supriya.osc.OscMessage(request_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return ["/status.reply"], None
