# -*- encoding: utf-8 -*-
from supriya.tools import servertools


class NRTNode(object):

    def __init__(self, session, session_id, start_offset=None):
        self.session = session
        self.session_id = int(session_id)
        self.start_offset = start_offset

    def add_group(self, add_action=None):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        node = nonrealtimetools.NRTGroup(
            self.session,
            session_id=len(self.session.nodes),
            start_offset=start_moment.timestep,
            )
        start_moment.start_nodes.add(node)
        self.move_node(node, add_action=add_action)
        return node

    def add_synth(self, duration=None, add_action=None):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        node = nonrealtimetools.NRTSynth(
            self.session,
            session_id=len(self.session.nodes),
            duration=duration,
            start_offset=start_moment.timestep,
            )
        start_moment.start_nodes.add(node)
        if node.duration:
            with self.session.at(node.stop_offset) as stop_moment:
                stop_moment.stop_nodes.add(node)
        self.move_node(node, add_action=add_action)
        return node

    def move_node(self, node, add_action=None):
        assert self.session.active_moments
        add_action = servertools.AddAction.from_expr(add_action)
        self.session.active_moments[-1]._register_action(
            source=node, target=self, action=add_action)
