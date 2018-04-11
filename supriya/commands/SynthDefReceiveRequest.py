import supriya.osc
from supriya.commands.Request import Request


class SynthDefReceiveRequest(Request):
    """
    A /d_recv request.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_completion_message',
        '_synthdefs',
        '_use_anonymous_names',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        completion_message=None,
        synthdefs=None,
        use_anonymous_names=None,
        ):
        import supriya.synthdefs
        Request.__init__(self)
        self._completion_message = completion_message
        if synthdefs:
            prototype = supriya.synthdefs.SynthDef
            if isinstance(synthdefs, prototype):
                synthdefs = (synthdefs,)
            assert all(isinstance(x, prototype) for x in synthdefs)
            synthdefs = tuple(synthdefs)
        self._synthdefs = synthdefs
        if use_anonymous_names is not None:
            use_anonymous_names = bool(use_anonymous_names)
        self._use_anonymous_names = use_anonymous_names

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        import supriya.synthdefs
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        compiled_synthdefs = supriya.synthdefs.SynthDefCompiler.compile_synthdefs(
            self.synthdefs,
            use_anonymous_names=self.use_anonymous_names,
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
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def completion_message(self):
        return self._completion_message

    @property
    def response_specification(self):
        import supriya.commands
        return {
            supriya.commands.DoneResponse: {
                'action': ('/d_recv',),
                },
            }

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.SYNTHDEF_RECEIVE

    @property
    def synthdefs(self):
        return self._synthdefs

    @property
    def use_anonymous_names(self):
        return self._use_anonymous_names
