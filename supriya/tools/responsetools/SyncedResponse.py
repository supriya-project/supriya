# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class SyncedResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sync_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        sync_id=None,
        osc_message=None,
        ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._sync_id = sync_id

    ### PUBLIC PROPERTIES ###

    @property
    def sync_id(self):
        return self._sync_id
