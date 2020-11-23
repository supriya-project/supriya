import supriya.osc
from .bases import Request
from supriya.enums import RequestId


class NothingRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NOTHING

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        return supriya.osc.OscMessage(0)
