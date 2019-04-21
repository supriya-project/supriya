import collections
import typing

import supriya.osc
from supriya.commands.Request import Request
from supriya.enums import RequestId
from supriya.realtime.Group import Group
from supriya.realtime.Node import Node


class GroupNewRequest(Request):
    """
    A /g_new request.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> group = supriya.Group().allocate()

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group

    ::

        >>> request = supriya.commands.GroupNewRequest(
        ...     items=[
        ...         supriya.commands.GroupNewRequest.Item(
        ...             add_action=supriya.AddAction.ADD_TO_TAIL,
        ...             node_id=1001,
        ...             target_node_id=1,
        ...             ),
        ...         supriya.commands.GroupNewRequest.Item(
        ...             add_action=supriya.AddAction.ADD_TO_HEAD,
        ...             node_id=1002,
        ...             target_node_id=1001,
        ...             ),
        ...         ],
        ...     )
        >>> request.to_osc(True)
        OscMessage('/g_new', 1001, 1, 1, 1002, 0, 1001)

    ::

        >>> with server.osc_io.capture() as transcript:
        ...     _ = request.communicate(server=server)
        ...     _ = server.sync()
        ...

    ::

        >>> for entry in transcript:
        ...     (entry.label, entry.message)
        ...
        ('S', OscMessage(21, 1001, 1, 1, 1002, 0, 1001))
        ('R', OscMessage('/n_go', 1001, 1, 1000, -1, 1, -1, -1))
        ('R', OscMessage('/n_go', 1002, 1001, -1, -1, 1, -1, -1))
        ('S', OscMessage(52, 0))
        ('R', OscMessage('/synced', 0))

    ::

        >>> print(server)
        NODE TREE 0 group
            1 group
                1000 group
                1001 group
                    1002 group

    ::

        >>> print(server.query_local_nodes())
        NODE TREE 0 group
            1 group
                1000 group
                1001 group
                    1002 group

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items",)

    class Item(typing.NamedTuple):
        add_action: int = 0
        node_id: int = 0
        target_node_id: int = 0

    request_id = RequestId.GROUP_NEW

    ### INITIALIZER ###

    def __init__(self, items=None):
        # TODO: Support multi-group allocation
        import supriya.realtime

        Request.__init__(self)
        if items:
            if not isinstance(items, collections.Sequence):
                items = [items]
            items = list(items)
            for i, (add_action, node_id, target_node_id) in enumerate(items):
                add_action = supriya.AddAction.from_expr(add_action)
                items[i] = self.Item(
                    add_action=add_action,
                    node_id=node_id,
                    target_node_id=target_node_id,
                )
        self._items = items

    ### PRIVATE METHODS ###

    def _apply_local(self, server):
        for item in self.items:
            if isinstance(item.node_id, Group):
                node_id = None
                group = item.node_id
            else:
                node_id = item.node_id
                group = Group()
            if isinstance(item.target_node_id, Node):
                target_node = item.target_node_id
            else:
                target_node = server._nodes[item.target_node_id]
            group._register_with_local_server(
                node_id=node_id,
                node_id_is_permanent=group.node_id_is_permanent,
                server=server,
            )
            target_node._move_node(add_action=item.add_action, node=group)

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        for item in self.items:
            contents.append(int(item.node_id))
            contents.append(int(item.add_action))
            contents.append(int(item.target_node_id))
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    @property
    def response_patterns(self):
        return ["/n_go", int(self.items[-1].node_id)], None
