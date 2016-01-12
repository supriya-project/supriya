# -*- encoding: utf-8 -*-
from supriya.tools import servertools


class NRTNode(object):

    def __init__(self, session, session_id):
        self.session = session
        self.session_id = int(session_id)

    def add_group(self, add_action=None):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        self.session.active_moments[-1].dirty = True
        node = nonrealtimetools.Group(
            self.session,
            len(self.session.nodes),
            )
        self.move_node(node, add_action=add_action)

    def add_synth(self, add_action=None):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        self.session.active_moments[-1].dirty = True
        node = nonrealtimetools.Synth(
            self.session,
            len(self.session.nodes),
            )
        self.move_node(node, add_action=add_action)

    def move_node(self, node, add_action=None):
        assert self.session.active_moments
        self.session.active_moments[-1].dirty = True
        add_action = servertools.AddAction.from_expr(add_action)
        assert add_action in self._valid_add_actions
        self.node_commands[node, self] = add_action
