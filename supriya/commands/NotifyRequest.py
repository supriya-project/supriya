import os
import supriya.osc
from supriya.commands.Request import Request


class NotifyRequest(Request):
    """
    A /notify message.

    ::

        >>> import supriya.commands

        >>> request = supriya.commands.NotifyRequest(
        ...     notify_status=True,
        ...     )
        >>> request
        NotifyRequest(
            notify_status=True,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(1, 1)

    ::

        >>> message.address == supriya.commands.RequestId.NOTIFY
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_notify_status',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        notify_status=None,
        ):
        Request.__init__(self)
        self._notify_status = bool(notify_status)

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        notify_status = int(self.notify_status)
        message = supriya.osc.OscMessage(
            request_id,
            notify_status,
            )
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def notify_status(self):
        return self._notify_status

    @property
    def response_specification(self):
        import supriya.commands
        pattern = ('/notify', 0)
        if os.environ.get('TRAVIS'):
            pattern = ('/notify',)
        return {
            supriya.commands.DoneResponse: {
                'action': pattern,
                },
            }

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.NOTIFY
