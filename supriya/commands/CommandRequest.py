from .bases import Request
from supriya.enums import RequestId


class CommandRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.COMMAND

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
