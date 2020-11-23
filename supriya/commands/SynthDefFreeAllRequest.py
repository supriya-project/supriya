from .bases import Request
from supriya.enums import RequestId


class SynthDefFreeAllRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTHDEF_FREE_ALL

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
