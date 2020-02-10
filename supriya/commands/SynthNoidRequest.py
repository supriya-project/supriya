from supriya.commands.Request import Request
from supriya.enums import RequestId


class SynthNoidRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNTH_NOID

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        raise NotImplementedError
