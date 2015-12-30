# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class SynthDefReceiveRequest(Request):
    r'''A /d_recv request.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_completion_message',
        '_synthdefs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        completion_message=None,
        synthdefs=None,
        ):
        from supriya.tools import synthdeftools
        Request.__init__(self)
        self._completion_message = completion_message
        if synthdefs:
            prototype = synthdeftools.SynthDef
            if isinstance(synthdefs, prototype):
                synthdefs = (synthdefs,)
            assert all(isinstance(x, prototype) for x in synthdefs)
            synthdefs = tuple(synthdefs)
        self._synthdefs = synthdefs

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        from supriya.tools import synthdeftools
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        compiled_synthdefs = synthdeftools.SynthDefCompiler.compile_synthdefs(
            self.synthdefs,
            )
        compiled_synthdefs = bytearray(compiled_synthdefs)
        contents = [
            request_id,
            compiled_synthdefs,
            ]
        if self.completion_message:
            completion_message = self.completion_message.to_datagram()
            completion_message = bytearray(completion_message)
            contents.append(completion_message)
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def completion_message(self):
        return self._completion_message

    @property
    def response_specification(self):
        from supriya.tools import responsetools
        return {
            responsetools.DoneResponse: {
                'action': ('/d_recv',),
                },
            }

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTHDEF_RECEIVE

    @property
    def synthdefs(self):
        return self._synthdefs
