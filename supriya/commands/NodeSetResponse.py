from typing import NamedTuple, Union

from supriya.commands.Response import Response


class NodeSetResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        '_node_id',
        )

    class Item(NamedTuple):
        control_index_or_name: Union[int, str]
        control_value: float

    ### INITIALIZER ###

    def __init__(
        self,
        node_id=None,
        items=None,
        osc_message=None,
    ):
        Response.__init__(self, osc_message=osc_message)
        self._items = items
        self._node_id = node_id

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response from OSC message.

        ::

            >>> message = supriya.osc.OscMessage('/n_set', 1023, '/one', -1, '/two', 0)
            >>> supriya.commands.NodeSetResponse.from_osc_message(message)
            NodeSetResponse(
                items=(
                    Item(control_index_or_name='/one', control_value=-1),
                    Item(control_index_or_name='/two', control_value=0),
                    ),
                node_id=1023,
                )

        """
        node_id, remainder = osc_message.contents[0], osc_message.contents[1:]
        items = []
        for group in cls._group_items(remainder, 2):
            item = cls.Item(*group)
            items.append(item)
        response = cls(
            node_id=node_id,
            items=tuple(items),
            )
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    @property
    def node_id(self):
        return self._node_id
