import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId


class SyncRequest(Request):
    """
    A /sync request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.SyncRequest(
        ...     sync_id=1999,
        ...     )
        >>> request
        SyncRequest(
            sync_id=1999,
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(52, 1999)

    ::

        >>> message.address == supriya.RequestId.SYNC
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_sync_id",)

    request_id = RequestId.SYNC

    ### INITIALIZER ###

    def __init__(self, sync_id=None):
        Request.__init__(self)
        self._sync_id = int(sync_id)

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        sync_id = int(self.sync_id)
        message = supriya.osc.OscMessage(request_id, sync_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return ["/synced", self.sync_id], None

    @property
    def sync_id(self):
        return self._sync_id
