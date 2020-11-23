import supriya.osc
from supriya.enums import RequestId

from .bases import Request


class ClearScheduleRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.CLEAR_SCHEDULE

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        message = supriya.osc.OscMessage(*contents)
        return message
