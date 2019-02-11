import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class QuitRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.QUIT

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        message = supriya.osc.OscMessage(request_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return [["/done", "/quit"]]
