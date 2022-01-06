from collections.abc import Sequence
from typing import NamedTuple, Tuple

import supriya.osc
from supriya.enums import RequestId

from .bases import Request, Response


class ControlBusFillRequest(Request):
    """
    A /c_fill request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.ControlBusFillRequest(
        ...     index_count_value_triples=[
        ...         (0, 8, 0.5),
        ...         (8, 8, 0.25),
        ...     ],
        ... )
        >>> request
        ControlBusFillRequest(
            index_count_value_triples=(
                (0, 8, 0.5),
                (8, 8, 0.25),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/c_fill', 0, 8, 0.5, 8, 8, 0.25)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.CONTROL_BUS_FILL

    ### INITIALIZER ###

    def __init__(self, index_count_value_triples=None):
        Request.__init__(self)
        if index_count_value_triples:
            triples = []
            for index, count, value in index_count_value_triples:
                index = int(index)
                count = int(count)
                value = float(value)
                assert 0 <= index
                assert 0 < count
                triple = (index, count, value)
                triples.append(triple)
            index_count_value_triples = tuple(triples)
        self._index_count_value_triples = index_count_value_triples

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        if self.index_count_value_triples:
            for index, count, value in self.index_count_value_triples:
                contents.append(index)
                contents.append(count)
                contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_count_value_triples(self):
        return self._index_count_value_triples


class ControlBusGetContiguousRequest(Request):
    """
    A /c_getn request.

    ::

        >>> server = supriya.Server().boot()
        >>> request = supriya.commands.ControlBusGetContiguousRequest(
        ...     index_count_pairs=[
        ...         (0, 2),
        ...         (4, 1),
        ...         (8, 2),
        ...         (12, 1),
        ...     ],
        ... )
        >>> request
        ControlBusGetContiguousRequest(
            index_count_pairs=(
                (0, 2),
                (4, 1),
                (8, 2),
                (12, 1),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/c_getn', 0, 2, 4, 1, 8, 2, 12, 1)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...
        ControlBusSetContiguousResponse(
            items=(
                Item(bus_values=(0.0, 0.0), starting_bus_id=0),
                Item(bus_values=(0.0,), starting_bus_id=4),
                Item(bus_values=(0.0, 0.0), starting_bus_id=8),
                Item(bus_values=(0.0,), starting_bus_id=12),
            ),
        )

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/c_getn', 0, 2, 4, 1, 8, 2, 12, 1))
        ('R', OscMessage('/c_setn', 0, 2, 0.0, 0.0, 4, 1, 0.0, 8, 2, 0.0, 0.0, 12, 1, 0.0))

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.CONTROL_BUS_GET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, index_count_pairs=None):
        Request.__init__(self)
        if index_count_pairs:
            pairs = []
            for index, count in index_count_pairs:
                index = int(index)
                count = int(count)
                assert 0 <= index
                assert 0 < count
                pair = (index, count)
                pairs.append(pair)
            index_count_pairs = tuple(pairs)
        self._index_count_pairs = index_count_pairs

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        if self.index_count_pairs:
            for pair in self.index_count_pairs:
                contents.extend(pair)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_count_pairs(self):
        return self._index_count_pairs

    @property
    def response_patterns(self):
        return ["/c_setn"], None


class ControlBusGetRequest(Request):
    """
    A /c_get request.

    ::

        >>> server = supriya.Server().boot()
        >>> request = supriya.commands.ControlBusGetRequest(
        ...     indices=(0, 4, 8, 12),
        ... )
        >>> request
        ControlBusGetRequest(
            indices=(0, 4, 8, 12),
        )

    ::

        >>> request.to_osc()
        OscMessage('/c_get', 0, 4, 8, 12)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...
        ControlBusSetResponse(
            items=(
                Item(bus_id=0, bus_value=0.0),
                Item(bus_id=4, bus_value=0.0),
                Item(bus_id=8, bus_value=0.0),
                Item(bus_id=12, bus_value=0.0),
            ),
        )

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/c_get', 0, 4, 8, 12))
        ('R', OscMessage('/c_set', 0, 0.0, 4, 0.0, 8, 0.0, 12, 0.0))

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.CONTROL_BUS_GET

    ### INITIALIZER ###

    def __init__(self, indices=None):
        Request.__init__(self)
        if indices:
            indices = tuple(int(index) for index in indices)
            assert all(0 <= index for index in indices)
        self._indices = indices

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        if self.indices:
            contents.extend(self.indices)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def indices(self):
        return self._indices

    @property
    def response_patterns(self):
        return ["/c_set"], None


class ControlBusSetContiguousRequest(Request):
    """
    A /c_setn request.

    ::

        >>> server = supriya.Server().boot()
        >>> request = supriya.commands.ControlBusSetContiguousRequest(
        ...     index_values_pairs=[
        ...         (0, (0.1, 0.2, 0.3)),
        ...         (4, (0.4, 0.5, 0.6)),
        ...     ],
        ... )
        >>> request
        ControlBusSetContiguousRequest(
            index_values_pairs=(
                (0, (0.1, 0.2, 0.3)),
                (4, (0.4, 0.5, 0.6)),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/c_setn', 0, 3, 0.1, 0.2, 0.3, 4, 3, 0.4, 0.5, 0.6)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/c_setn', 0, 3, 0.1, 0.2, 0.3, 4, 3, 0.4, 0.5, 0.6))
        ('S', OscMessage('/sync', 0))
        ('R', OscMessage('/synced', 0))

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.CONTROL_BUS_SET_CONTIGUOUS

    ### INITIALIZER ###

    def __init__(self, index_values_pairs=None):
        Request.__init__(self)
        if index_values_pairs:
            pairs = []
            for index, values in index_values_pairs:
                index = int(index)
                values = tuple(float(value) for value in values)
                assert 0 <= index
                assert values
                if not values:
                    continue
                pair = (index, values)
                pairs.append(pair)
            index_values_pairs = tuple(pairs)
        self._index_values_pairs = index_values_pairs

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for starting_bus_index, values in self._index_values_pairs or ():
            for i, value in enumerate(values):
                bus_id = starting_bus_index + i
                bus_proxy = server._get_control_bus_proxy(bus_id)
                bus_proxy._value = value

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        if self.index_values_pairs:
            for index, values in self.index_values_pairs:
                contents.append(index)
                contents.append(len(values))
                contents.extend(values)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_values_pairs(self):
        return self._index_values_pairs


class ControlBusSetContiguousResponse(Response, Sequence):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        bus_values: Tuple[float]
        starting_bus_id: int

    ### INITIALIZER ###

    def __init__(self, items=None):
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        items = []
        contents = list(osc_message.contents)
        while contents:
            starting_bus_id = contents[0]
            bus_count = contents[1]
            bus_values = tuple(contents[2 : 2 + bus_count])
            item = cls.Item(starting_bus_id=starting_bus_id, bus_values=bus_values)
            items.append(item)
            contents = contents[2 + bus_count :]
        items = tuple(items)
        response = cls(items=items)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items


class ControlBusSetRequest(Request):
    """
    A /c_set request.

    ::

        >>> server = supriya.Server().boot()
        >>> request = supriya.commands.ControlBusSetRequest(
        ...     index_value_pairs=[
        ...         (0, 0.1),
        ...         (1, 0.2),
        ...         (2, 0.3),
        ...         (3, 0.4),
        ...     ],
        ... )
        >>> request
        ControlBusSetRequest(
            index_value_pairs=(
                (0, 0.1),
                (1, 0.2),
                (2, 0.3),
                (3, 0.4),
            ),
        )

    ::

        >>> request.to_osc()
        OscMessage('/c_set', 0, 0.1, 1, 0.2, 2, 0.3, 3, 0.4)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/c_set', 0, 0.1, 1, 0.2, 2, 0.3, 3, 0.4))
        ('S', OscMessage('/sync', 0))
        ('R', OscMessage('/synced', 0))


    """

    ### CLASS VARIABLES ###

    request_id = RequestId.CONTROL_BUS_SET

    ### INITIALIZER ###

    def __init__(self, index_value_pairs=None):
        Request.__init__(self)
        if index_value_pairs:
            pairs = []
            for index, value in index_value_pairs:
                index = int(index)
                value = float(value)
                assert 0 <= index
                pair = (index, value)
                pairs.append(pair)
            index_value_pairs = tuple(pairs)
        self._index_value_pairs = index_value_pairs

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for bus_id, value in self.index_value_pairs or ():
            bus_proxy = server._get_control_bus_proxy(bus_id)
            bus_proxy._value = value

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        if self.index_value_pairs:
            for pair in self.index_value_pairs:
                contents.extend(pair)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def index_value_pairs(self):
        return self._index_value_pairs


class ControlBusSetResponse(Response, Sequence):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        bus_id: int
        bus_value: float

    ### INITIALIZER ###

    def __init__(self, items=None):
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        items = []
        for group in cls._group_items(osc_message.contents, 2):
            item = cls.Item(*group)
            items.append(item)
        response = cls(items=tuple(items))
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items
