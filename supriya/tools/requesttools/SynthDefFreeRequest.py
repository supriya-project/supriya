# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class SynthDefFreeRequest(Request):
    r'''A /d_free request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.SynthDefFreeRequest(
        ...     synthdef='test',
        ...     )
        >>> request
        SynthDefFreeRequest(
            synthdef='test'
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(53, 'test')

    ::

        >>> message.address == requesttools.RequestId.SYNTHDEF_FREE
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef=None,
        ):
        from supriya.tools import synthdeftools
        Request.__init__(self)
        prototype = (str, synthdeftools.SynthDef)
        assert isinstance(synthdef, prototype)
        self._synthdef = synthdef

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        from supriya.tools import synthdeftools
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        synthdef = self.synthdef
        if isinstance(synthdef, synthdeftools.SynthDef):
            synthdef = synthdef.actual_name
        message = osctools.OscMessage(
            request_id,
            synthdef,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTHDEF_FREE

    @property
    def synthdef(self):
        return self._synthdef
