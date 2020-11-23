import supriya.osc
from supriya.enums import RequestId

from .bases import Request


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

        >>> request.to_osc()
        OscMessage('/sync', 1999)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNC

    ### INITIALIZER ###

    def __init__(self, sync_id=None):
        Request.__init__(self)
        self._sync_id = int(sync_id)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
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
