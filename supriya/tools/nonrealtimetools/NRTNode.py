# -*- encoding: utf-8 -*-
from supriya.tools import servertools


class NRTNode(object):

    def __init__(self, session, session_id):
        self.session = session
        self.session_id = int(session_id)

    def add_group(self, add_action=None):
        from supriya.tools import nonrealtimetools
        node = nonrealtimetools.NRTGroup(
            self.session,
            len(self.session.nodes),
            )
        self.move_node(node, add_action=add_action)

    def add_synth(self, duration=None, add_action=None):
        from supriya.tools import nonrealtimetools
        node = nonrealtimetools.NRTSynth(
            self.session,
            duration,
            len(self.session.nodes),
            )
        self.move_node(node, add_action=add_action)

    def move_node(self, node, add_action=None):
        assert self.session.active_moments
        self.session.active_moments[-1].dirty = True
        add_action = servertools.AddAction.from_expr(add_action)
        self.session.active_moments[-1]._register_action(
            source=node, target=self, action=add_action)
