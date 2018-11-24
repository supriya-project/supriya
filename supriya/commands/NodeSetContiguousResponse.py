from typing import NamedTuple, Tuple, Union

from supriya.commands.Response import Response


class NodeSetContiguousResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = ("_items", "_node_id")

    class Item(NamedTuple):
        control_values: Tuple[float]
        starting_control_index_or_name: Union[int, str]

    ### INITIALIZER ###

    def __init__(self, node_id=None, items=None, osc_message=None):
        Response.__init__(self, osc_message=osc_message)
        self._items = items
        self._node_id = node_id

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        node_id, remainder = osc_message.contents[0], osc_message.contents[1:]
        items = []
        while remainder:
            control_index_or_name = remainder[0]
            control_count = remainder[1]
            control_values = tuple(remainder[2 : 2 + control_count])
            item = cls.Item(
                control_index_or_name=control_index_or_name,
                control_values=control_values,
            )
            items.append(item)
            remainder = remainder[2 + control_count :]
        items = tuple(items)
        response = cls(node_id=node_id, items=items)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    @property
    def node_id(self):
        return self._node_id
