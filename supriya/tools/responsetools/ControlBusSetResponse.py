# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.ServerResponse import ServerResponse


class ControlBusSetResponse(ServerResponse):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        ):
        self._items = items

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items
