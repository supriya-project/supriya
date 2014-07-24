# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class SynthdefFreeRequest(Request):
    r'''A /d_free request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.SynthdefFreeRequest(
        ...     synthdef_name='test',
        ...     )
        >>> request
        SynthdefFreeRequest(
            synthdef_name='test'
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
        '_synthdef_name', 
        )

    ### INITIALIZER ###

    def __init__(
        self,
        synthdef_name=None,
        ):
        self._synthdef_name = synthdef_name

    ### PUBLIC METHODS ###

    def to_osc_message(self):
        request_id = int(self.request_id)
        message = osctools.OscMessage(
            request_id,
            self.synthdef_name,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_prototype(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.SYNTHDEF_FREE

    @property
    def synthdef_name(self):
        return self._synthdef_name