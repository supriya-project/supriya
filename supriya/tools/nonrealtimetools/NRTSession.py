# -*- encoding: utf-8 -*-
from supriya.tools import servertools
from supriya.tools import timetools


class NRTSession(object):

    _valid_add_actions = (
        servertools.AddAction.ADD_TO_HEAD,
        servertools.AddAction.ADD_TO_TAIL,
        )

    def __init__(self):
        from supriya.tools import nonrealtimetools
        self.nodes = timetools.TimespanCollection()
        self.active_moments = []
        self.moments = {}
        self.states = []
        self.root_node = nonrealtimetools.NRTRootNode(self)
        initial_moment = nonrealtimetools.NRTMoment(self, 0)
        initial_moment.nodes_to_children[self.root_node] = []
        initial_moment.nodes_to_parent[self.root_node] = None
        self.moments[0] = initial_moment

    def at(self, timestep):
        from supriya.tools import nonrealtimetools
        assert 0 <= timestep
        if timestep in self.moments:
            return self.moments[timestep]
        return nonrealtimetools.NRTMoment(self, timestep)

    def add_group(self, add_action=None):
        self.root_node.add_group(add_action=add_action)

    def add_synth(self, duration=None, add_action=None):
        self.root_node.add_synth(duration=duration, add_action=add_action)

    def move_node(self, node, add_action=None):
        self.root_node.move_node(node, add_action=add_action)
