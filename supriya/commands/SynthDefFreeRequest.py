from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class SynthDefFreeRequest(Request):
    """
    A /d_free request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.SynthDefFreeRequest(
        ...     synthdef='test',
        ...     )
        >>> request
        SynthDefFreeRequest(
            synthdef='test',
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(53, 'test')

    ::

        >>> message.address == supriya.commands.RequestId.SYNTHDEF_FREE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ('_synthdef',)

    request_id = RequestId.SYNTHDEF_FREE

    ### INITIALIZER ###

    def __init__(self, synthdef=None):
        import supriya.synthdefs

        Request.__init__(self)
        prototype = (str, supriya.synthdefs.SynthDef)
        assert isinstance(synthdef, prototype)
        self._synthdef = synthdef

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        import supriya.synthdefs

        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        synthdef = self.synthdef
        if isinstance(synthdef, supriya.synthdefs.SynthDef):
            synthdef = synthdef.actual_name
        message = supriya.osc.OscMessage(request_id, synthdef)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef
