from supriya.commands.Response import Response


class SyncedResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = ("_sync_id",)

    ### INITIALIZER ###

    def __init__(self, sync_id=None, osc_message=None):
        Response.__init__(self, osc_message=osc_message)
        self._sync_id = sync_id

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = osc_message.contents
        response = cls(*arguments)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def sync_id(self):
        return self._sync_id
