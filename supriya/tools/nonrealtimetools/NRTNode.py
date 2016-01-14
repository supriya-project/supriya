# -*- encoding: utf-8 -*-
from supriya.tools import servertools


class NRTNode(object):

    ### INITIALIZER ###

    def __init__(self, session, session_id, start_offset=None):
        self.session = session
        self.session_id = int(session_id)
        self.start_offset = start_offset
        self.duration = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<{} #{} @{}:{}>'.format(
            type(self).__name__,
            self.session_id,
            self.start_offset,
            self.stop_offset,
            )

    ### PUBLIC METHODS ###
        
    def add_group(self, add_action=None):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        node = nonrealtimetools.NRTGroup(
            self.session,
            session_id=len(self.session.nodes) + 1,
            start_offset=start_moment.timestep,
            )
        self.move_node(node, add_action=add_action)
        start_moment.start_nodes.add(node)
        self.session.nodes.add(node)
        return node

    def add_synth(self, duration=None, add_action=None):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        node = nonrealtimetools.NRTSynth(
            self.session,
            session_id=len(self.session.nodes) + 1,
            duration=duration,
            start_offset=start_moment.timestep,
            )
        self.move_node(node, add_action=add_action)
        start_moment.start_nodes.add(node)
        if node.duration:
            with self.session.at(node.stop_offset) as stop_moment:
                stop_moment.stop_nodes.add(node)
        self.session.nodes.add(node)
        return node

    def move_node(self, node, add_action=None):
        assert self.session.active_moments
        add_action = servertools.AddAction.from_expr(add_action)
        self.session.active_moments[-1]._register_action(
            source=node,
            target=self,
            action=add_action,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def stop_offset(self):
        if self.duration is None:
            return None
        return self.start_offset + self.duration
