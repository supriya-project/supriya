# -*- encoding: utf-8 -*-
from supriya.tools.responselib.ServerResponse import ServerResponse


class SyncedResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sync_id',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        sync_id=None,
        ):
        self._sync_id = sync_id

    ### PUBLIC PROPERTIES ###

    @property
    def sync_id(self):
        return self._sync_id
