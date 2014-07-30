# -*- encoding: utf-8 -*-
import collections
from supriya.tools.servertools.Node import Node


class Group(Node, collections.Sequence):
    r'''A group.

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server()
        >>> server.boot()
        <Server: udp://127.0.0.1:57751, 8i8o>

    ::

        >>> group = servertools.Group()
        >>> group.allocate()
        <Group: 1000>

    ::

        >>> group.free()
        <Group: ???>

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_children',
        '_named_children',
        )

    ### INITIALIZER ###

    def __init__(self):
        Node.__init__(self)
        self._children = []
        self._named_children = {}

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._children[item]

    def __len__(self):
        return len(self._children)

    ### PRIVATE METHODS ###

    @staticmethod
    def _iterate_children(group):
        from supriya.tools import servertools
        for child in group.children:
            if isinstance(child, servertools.Group):
                for subchild in Group._iterate_children(child):
                    yield subchild
            yield child

    ### PUBLIC METHODS ###

    def allocate(
        self,
        add_action=None,
        node_id_is_permanent=False,
        sync=False,
        target_node=None,
        ):
        from supriya.tools import requesttools
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            node_id_is_permanent=node_id_is_permanent,
            target_node=target_node,
            )
        request = requesttools.GroupNewRequest(
            add_action=add_action,
            node_id=node_id,
            target_node_id=target_node_id,
            )
        message = request.to_osc_message()
        self.server.send_message(message)
        if sync:
            self.server.sync()
        return self

    def free(
        self,
        send_to_server=True,
        ):
        for child in self.children:
            child.free(
                send_to_server=False,
                )
        Node.free(
            self,
            send_to_server=send_to_server,
            )
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)