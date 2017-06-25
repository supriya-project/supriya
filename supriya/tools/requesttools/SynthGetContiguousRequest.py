from supriya.tools.requesttools.Request import Request


class SynthGetContiguousRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTH_GET_CONTIGUOUS
