# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class DumpOscRequest(Request):
    """
    A /dumpOSC request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.DumpOscRequest(1)
        >>> request
        DumpOscRequest(
            osc_status=1
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(39, 1)

    ::

        >>> message.address == requesttools.RequestId.DUMP_OSC
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_osc_status',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        osc_status=None,
        ):
        Request.__init__(self)
        self._osc_status = int(osc_status)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        osc_status = int(self.osc_status)
        assert 0 <= osc_status <= 4
        message = osctools.OscMessage(
            request_id,
            osc_status,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def osc_status(self):
        return self._osc_status

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.DUMP_OSC
