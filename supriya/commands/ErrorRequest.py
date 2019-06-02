from supriya.commands.Request import Request
from supriya.enums import RequestId


class ErrorRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.ERROR

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        raise NotImplementedError
