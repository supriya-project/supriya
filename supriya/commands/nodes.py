from collections.abc import Sequence
from typing import NamedTuple, Tuple, Union

import supriya.osc
from supriya.enums import NodeAction, RequestId

from .bases import Request, Response


class NodeFreeRequest(Request):
    """
    A /n_free request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.NodeFreeRequest(
        ...     node_ids=1000,
        ... )
        >>> request
        NodeFreeRequest(
            node_ids=(1000,),
        )

    ::

        >>> request.to_osc()
        OscMessage('/n_free', 1000)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_FREE

    ### INITIALIZER ###

    def __init__(self, node_ids=None):
        Request.__init__(self)
        if not isinstance(node_ids, Sequence):
            node_ids = (node_ids,)
        node_ids = tuple(int(_) for _ in node_ids)
        self._node_ids = node_ids

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for node_id in self.node_ids:
            node = server._nodes.get(node_id)
            if not node:
                continue
            node._set_parent(None)
            node._unregister_with_local_server()

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id, *self.node_ids]
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_ids(self):
        return self._node_ids

    @property
    def response_patterns(self):
        return ["/n_end", int(self.node_ids[-1])], None


class NodeInfoResponse(Response):

    ### INITIALIZER ###

    def __init__(
        self,
        action=None,
        node_id=None,
        parent_id=None,
        previous_node_id=None,
        next_node_id=None,
        is_group=None,
        head_node_id=None,
        tail_node_id=None,
        synthdef_name=None,
        synthdef_controls=None,
    ):
        self._action = NodeAction.from_address(action)
        self._is_group = bool(is_group)
        self._head_node_id = self._coerce_node_id(head_node_id)
        self._next_node_id = self._coerce_node_id(next_node_id)
        self._node_id = self._coerce_node_id(node_id)
        self._parent_id = self._coerce_node_id(parent_id)
        self._previous_node_id = self._coerce_node_id(previous_node_id)
        self._tail_node_id = self._coerce_node_id(tail_node_id)
        self._synthdef_name = synthdef_name
        self._synthdef_controls = synthdef_controls

    ### PRIVATE METHODS ###

    def _coerce_node_id(self, node_id):
        if node_id is not None and -1 < node_id:
            return node_id
        return None

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = (osc_message.address,) + osc_message.contents
        kwargs = dict(
            action=arguments[0],
            node_id=arguments[1],
            parent_id=arguments[2],
            previous_node_id=arguments[3],
            next_node_id=arguments[4],
            is_group=arguments[5],
        )
        if arguments[5]:
            kwargs.update(head_node_id=arguments[6], tail_node_id=arguments[7])
        elif len(arguments) > 6:
            controls = []
            for i in range(arguments[7]):
                controls.append((arguments[8 + (i * 2)], arguments[9 + (i * 2)]))
            kwargs.update(synthdef_name=arguments[6], synthdef_controls=tuple(controls))
        response = cls(**kwargs)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action

    @property
    def head_node_id(self):
        return self._head_node_id

    @property
    def is_group(self):
        return self._is_group

    @property
    def next_node_id(self):
        return self._next_node_id

    @property
    def node_id(self):
        return self._node_id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def previous_node_id(self):
        return self._previous_node_id

    @property
    def tail_node_id(self):
        return self._tail_node_id

    @property
    def synthdef_controls(self):
        return self._synthdef_controls

    @property
    def synthdef_name(self):
        return self._synthdef_name


class NodeMapToAudioBusRequest(Request):
    """
    A /n_mapa request.

    ::

        >>> import supriya.commands
        >>> import supriya.realtime
        >>> request = supriya.commands.NodeMapToAudioBusRequest(
        ...     node_id=1000,
        ...     frequency=supriya.realtime.Bus(9, "audio"),
        ...     phase=supriya.realtime.Bus(10, "audio"),
        ...     amplitude=supriya.realtime.Bus(11, "audio"),
        ... )
        >>> request
        NodeMapToAudioBusRequest(
            amplitude=<- Bus: 11 (audio)>,
            frequency=<- Bus: 9 (audio)>,
            node_id=1000,
            phase=<- Bus: 10 (audio)>,
        )

    ::

        >>> request.to_osc()
        OscMessage('/n_mapa', 1000, 'amplitude', 11, 'frequency', 9, 'phase', 10)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_MAP_TO_AUDIO_BUS

    ### INITIALIZER ###

    def __init__(self, node_id=None, **kwargs):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = dict((name, value) for name, value in kwargs.items())

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = self._sanitize_node_id(self.node_id, with_placeholders)
        contents = []
        for name, bus in sorted(self._kwargs.items()):
            contents.append(name)
            contents.append(int(bus))
        message = supriya.osc.OscMessage(request_id, node_id, *contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id


class NodeMapToControlBusRequest(Request):
    """
    A /n_map request.

    ::

        >>> import supriya.commands
        >>> import supriya.realtime
        >>> request = supriya.commands.NodeMapToControlBusRequest(
        ...     node_id=1000,
        ...     frequency=supriya.realtime.Bus(9, "control"),
        ...     phase=supriya.realtime.Bus(10, "control"),
        ...     amplitude=supriya.realtime.Bus(11, "control"),
        ... )
        >>> request
        NodeMapToControlBusRequest(
            amplitude=<- Bus: 11 (control)>,
            frequency=<- Bus: 9 (control)>,
            node_id=1000,
            phase=<- Bus: 10 (control)>,
        )

    ::

        >>> request.to_osc()
        OscMessage('/n_map', 1000, 'amplitude', 11, 'frequency', 9, 'phase', 10)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_MAP_TO_CONTROL_BUS

    ### INITIALIZER ###

    def __init__(self, node_id=None, **kwargs):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = dict((name, value) for name, value in kwargs.items())

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = self._sanitize_node_id(self.node_id, with_placeholders)
        contents = []
        for name, bus in sorted(self._kwargs.items()):
            contents.append(name)
            contents.append(int(bus))
        message = supriya.osc.OscMessage(request_id, node_id, *contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id


class NodeQueryRequest(Request):
    """
    A /n_query request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.NodeQueryRequest(
        ...     node_id=1000,
        ... )
        >>> request
        NodeQueryRequest(
            node_id=1000,
        )

    ::

        >>> request.to_osc()
        OscMessage('/n_query', 1000)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_QUERY

    ### INITIALIZER ###

    def __init__(self, node_id=None):
        Request.__init__(self)
        self._node_id = node_id

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = int(self.node_id)
        message = supriya.osc.OscMessage(request_id, node_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def response_patterns(self):
        return ["/n_info", self.node_id], ["/fail"]


class NodeRunRequest(Request):
    """
    A /n_run request.

    ::

        >>> server = supriya.Server().boot()
        >>> synth_a = supriya.Synth().allocate(server)
        >>> synth_b = supriya.Synth().allocate(server)
        >>> synth_a.is_paused, synth_b.is_paused
        (False, False)

    Unpause ``synth_a`` (a no-op because it's already unpaused) and pause
    ``synth_b``:

    ::

        >>> request = supriya.commands.NodeRunRequest(
        ...     [
        ...         [synth_a, True],
        ...         [synth_b, False],
        ...     ]
        ... )
        >>> request.to_osc()
        OscMessage('/n_run', 1000, 1, 1001, 0)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/n_run', 1000, 1, 1001, 0))
        ('S', OscMessage('/sync', 0))
        ('R', OscMessage('/n_off', 1001, 1, -1, 1000, 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> synth_a.is_paused, synth_b.is_paused
        (False, True)

    Pause ``synth_a`` and unpause ``synth_b``:

    ::

        >>> request = supriya.commands.NodeRunRequest(
        ...     [
        ...         [synth_a, False],
        ...         [synth_b, True],
        ...     ]
        ... )
        >>> request.to_osc()
        OscMessage('/n_run', 1000, 0, 1001, 1)

    ::

        >>> with server.osc_protocol.capture() as transcript:
        ...     request.communicate(server=server)
        ...     _ = server.sync()
        ...
        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage('/n_run', 1000, 0, 1001, 1))
        ('S', OscMessage('/sync', 1))
        ('R', OscMessage('/n_off', 1000, 1, 1001, -1, 0))
        ('R', OscMessage('/n_on', 1001, 1, -1, 1000, 0))
        ('R', OscMessage('/synced', 1))

    ::

        >>> synth_a.is_paused, synth_b.is_paused
        (True, False)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_RUN

    ### INITIALIZER ###

    def __init__(self, node_id_run_flag_pairs=None):
        Request.__init__(self)
        if node_id_run_flag_pairs:
            pairs = []
            for node_id, run_flag in node_id_run_flag_pairs:
                node_id = node_id
                run_flag = bool(run_flag)
                pairs.append((node_id, run_flag))
            node_id_run_flag_pairs = tuple(pairs)
        self._node_id_run_flag_pairs = node_id_run_flag_pairs

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for node_id, run_flag in self.node_id_run_flag_pairs:
            node = server._nodes.get(node_id)
            if not node:
                continue
            node._run(run_flag)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        sanitized_pairs = []
        for node_id, run_flag in self.node_id_run_flag_pairs or []:
            node_id = self._sanitize_node_id(node_id, with_placeholders)
            sanitized_pairs.append((node_id, int(run_flag)))
        for pair in sorted(sanitized_pairs):
            contents.extend(pair)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id_run_flag_pairs(self):
        return self._node_id_run_flag_pairs


class NodeSetRequest(Request):
    """
    A /n_set request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.NodeSetRequest(
        ...     1000,
        ...     frequency=443.1,
        ...     phase=0.5,
        ...     amplitude=0.1,
        ... )
        >>> request
        NodeSetRequest(
            amplitude=0.1,
            frequency=443.1,
            node_id=1000,
            phase=0.5,
        )

    ::

        >>> request.to_osc()
        OscMessage('/n_set', 1000, 'amplitude', 0.1, 'frequency', 443.1, 'phase', 0.5)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NODE_SET

    ### INITIALIZER ###

    def __init__(self, node_id=None, **kwargs):
        Request.__init__(self)
        self._node_id = node_id
        self._kwargs = kwargs

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]
        return object.__getattr__(self, name)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        node_id = int(self.node_id)
        contents = [request_id, node_id]
        for key, value in sorted(self._kwargs.items()):
            contents.append(key)
            contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id


class NodeSetResponse(Response):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        control_index_or_name: Union[int, str]
        control_value: float

    ### INITIALIZER ###

    def __init__(self, node_id=None, items=None):
        self._items = items
        self._node_id = node_id

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response from OSC message.

        ::

            >>> message = supriya.osc.OscMessage("/n_set", 1023, "/one", -1, "/two", 0)
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
        response = cls(node_id=node_id, items=tuple(items))
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    @property
    def node_id(self):
        return self._node_id


class NodeSetContiguousResponse(Response):

    ### CLASS VARIABLES ###

    class Item(NamedTuple):
        control_values: Tuple[float]
        starting_control_index_or_name: Union[int, str]

    ### INITIALIZER ###

    def __init__(self, node_id=None, items=None):
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
