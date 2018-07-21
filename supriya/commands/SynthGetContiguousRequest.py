from supriya.commands.Request import Request


class SynthGetContiguousRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc(self, with_textual_osc_command=False):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.SYNTH_GET_CONTIGUOUS
