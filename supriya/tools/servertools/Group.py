# -*- encoding: utf-8 -*-
from supriya.tools.servertools.Node import Node


class Group(Node):
    r'''A group.

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server().boot()
        RECV: DoneResponse(
            action=('/notify', 0)
            )

    ::

        >>> group = servertools.Group()
        >>> group.allocate()
        <Group: 1000>

    ::

        >>> group.free()
        <Group: ???>

    ::

        >>> server = server.quit()
        RECV: NodeInfoResponse(
            action=<NodeAction.NODE_CREATED: 0>,
            node_id=1,
            parent_group_id=0,
            is_group=True
            )
        RECV: NodeInfoResponse(
            action=<NodeAction.NODE_CREATED: 0>,
            node_id=1000,
            parent_group_id=1,
            is_group=True
            )
        RECV: NodeInfoResponse(
            action=<NodeAction.NODE_REMOVED: 1>,
            node_id=1000,
            parent_group_id=1,
            is_group=True
            )
        RECV: DoneResponse(
            action=('/quit',)
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_children',
        )

    ### INITIALIZER ###

    def __init__(self):
        Node.__init__(self)
        self._children = []

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
        target_node=None,
        ):
        from supriya.tools import servertools
        add_action, node_id, target_node_id = Node.allocate(
            self,
            add_action=add_action,
            target_node=target_node,
            )
        message = servertools.CommandManager.make_group_new_message(
            add_action=add_action,
            node_id=node_id,
            target_node_id=target_node_id,
            )
        self.server.send_message(message)
        return self

    def free(self, send_to_server=True):
        for child in self.children:
            child.free(send_to_server=False)
        Node.free(self, send_to_server=send_to_server)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)