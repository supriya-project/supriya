from supriya.enums import RequestId

from .bases import Request


class CommandRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.COMMAND

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
