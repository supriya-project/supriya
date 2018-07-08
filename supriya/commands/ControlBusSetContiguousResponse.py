import collections
from supriya.commands.Response import Response


class ControlBusSetContiguousResponse(Response, collections.Sequence):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None, osc_message=None):
        Response.__init__(self, osc_message=osc_message)
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        import supriya.commands
        items = []
        while osc_message.contents:
            starting_bus_id = osc_message.contents[0]
            bus_count = osc_message.contents[1]
            bus_values = tuple(osc_message.contents[2:2 + bus_count])
            item = supriya.commands.ControlBusSetContiguousItem(
                starting_bus_id=starting_bus_id,
                bus_values=bus_values,
                )
            items.append(item)
            osc_message.contents = osc_message.contents[2 + bus_count:]
        items = tuple(items)
        response = cls(items=items)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items
