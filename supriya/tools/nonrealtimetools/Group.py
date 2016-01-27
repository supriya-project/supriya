# -*- encoding: utf-8 -*-
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.Node import Node


class Group(Node):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _valid_add_actions = (
        servertools.AddAction.ADD_TO_HEAD,
        servertools.AddAction.ADD_TO_TAIL,
        servertools.AddAction.ADD_AFTER,
        servertools.AddAction.ADD_BEFORE,
        )

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'group-{}'.format(self.session_id)

    ### PUBLIC METHODS ###

    def to_request(self, action, id_mapping):
        source_id = id_mapping[action.source]
        target_id = id_mapping[action.target]
        add_action = action.action
        request = requesttools.GroupNewRequest(
            add_action=add_action,
            node_id=source_id,
            target_node_id=target_id,
            )
        return request
