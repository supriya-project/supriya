from supriya.commands.Request import Request
from supriya.enums import RequestId


class SynthDefFreeAllRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    request_id = RequestId.SYNTHDEF_FREE_ALL

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False, with_request_name=False):
        raise NotImplementedError
