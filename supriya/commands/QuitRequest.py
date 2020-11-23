import supriya.osc
from supriya.enums import RequestId

from .bases import Request


class QuitRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.QUIT

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        message = supriya.osc.OscMessage(request_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return ["/done", "/quit"], None
