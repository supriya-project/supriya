# -*- encoding: utf-8 -*-
from supriya.tools.servertools.GroupMixin import GroupMixin
from supriya.tools.servertools.Node import Node


class Group(GroupMixin, Node):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_children',
        )

    ### INITIALIZER ###

    def __init__(self):
        Node.__init__(self)
        GroupMixin.__init__(self)

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

    def free(self, send_to_server=True):
        for child in self.children:
            child.free(send_to_server=False)
        Node.free(self, send_to_server=send_to_server)
