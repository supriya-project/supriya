import supriya.osc
from supriya.commands.Request import Request


class DumpOscRequest(Request):
    """
    A /dumpOSC request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.DumpOscRequest(1)
        >>> request
        DumpOscRequest(
            osc_status=1,
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(39, 1)

    ::

        >>> message.address == supriya.commands.RequestId.DUMP_OSC
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_osc_status',
        )

    ### INITIALIZER ###

    def __init__(self, osc_status=None):
        Request.__init__(self)
        self._osc_status = int(osc_status)

    ### PUBLIC METHODS ###

    def to_osc(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        osc_status = int(self.osc_status)
        assert 0 <= osc_status <= 4
        message = supriya.osc.OscMessage(
            request_id,
            osc_status,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def osc_status(self):
        return self._osc_status

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.DUMP_OSC
