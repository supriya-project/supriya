# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class SynthdefReceiveRequest(Request):
    r'''A /d_recv request.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdefs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdefs=None,
        ):
        from supriya.tools import synthdeftools
        if synthdefs:
            prototype = synthdeftools.SynthDef 
            assert all(isinstance(x, prototype) for x in synthdefs)
            synthdefs = tuple(synthdefs)
        self._synthdefs = synthdefs

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        from supriya.tools import synthdeftools
        request_id = int(self.request_id)
        compiled_synthdefs = synthdeftools.SynthDefCompiler.compile_synthdefs(
            self.synthdefs,
            )
        compiled_synthdefs = bytearray(compiled_synthdefs)
        message = osctools.OscMessage(
            request_id,
            compiled_synthdefs,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTHDEF_RECEIVE

    @property
    def synthdefs(self):
        return self._synthdefs