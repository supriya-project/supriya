# -*- encoding: utf-8 -*-
from supriya.tools.requesttools.Request import Request


class SynthDefLoadRequest(Request):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTHDEF_LOAD