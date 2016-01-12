# -*- encoding: utf-8 -*-
from supriya.tools import timetools


class NRTSession(object):

    def __init__(self):
        from supriya.tools import nonrealtimetools
        self.nodes = timetools.TimespanCollection()
        self.active_moments = []
        self.moments = []
        self.states = []
        self.root_node = nonrealtimetools.NRTRootNode(self)
        initial_moment = nonrealtimetools.NRTMoment(self, 0)
        initial_moment.nodes_to_children[self.root_node] = []
        initial_moment.nodes_to_parent[self.root_node] = None
        self.moments.append(initial_moment)

    def at(self, timestep):
        from supriya.tools import nonrealtimetools
        return nonrealtimetools.NRTMoment(self, timestep)
