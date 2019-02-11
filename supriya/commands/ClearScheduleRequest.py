import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class ClearScheduleRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.CLEAR_SCHEDULE

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        message = supriya.osc.OscMessage(*contents)
        return message
