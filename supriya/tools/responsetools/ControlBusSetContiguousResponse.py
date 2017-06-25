import collections
from supriya.tools.responsetools.Response import Response


class ControlBusSetContiguousResponse(Response, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        osc_message=None,
        ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items
