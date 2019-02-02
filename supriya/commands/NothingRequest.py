import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class NothingRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NOTHING

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        return supriya.osc.OscMessage(0)
