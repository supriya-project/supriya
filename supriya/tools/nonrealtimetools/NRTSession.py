# -*- encoding: utf-8 -*-
import bisect
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
        self.root_node = nonrealtimetools.NRTRootNode(self)
        initial_moment = nonrealtimetools.NRTMoment(self, 0)
        initial_moment.nodes_to_children[self.root_node] = []
        initial_moment.nodes_to_parent[self.root_node] = None
        self.moments[0] = initial_moment
        self.timesteps = [0]

    ### PRIVATE METHODS ###

    def _find_moment_after(self, timestep):
        index = bisect.bisect(self.timesteps, timestep)
        if index < len(self.timesteps):
            old_timestep = self.timesteps[index]
            if timestep < old_timestep:
                return self.moments[old_timestep]
        return None

    def _find_moment_at(self, timestep):
        return self.moments.get(timestep, None)

    def _find_moment_before(self, timestep):
        index = bisect.bisect_left(self.timesteps, timestep)
        if index == len(self.timesteps):
            index -= 1
        old_timestep = self.timesteps[index]
        if timestep <= old_timestep:
            index -= 1
        if index < 0:
            return None
        old_timestep = self.timesteps[index]
        return self.moments[old_timestep]

    ### PUBLIC METHODS ###

    def at(self, timestep):
        assert 0 <= timestep
        moment = self._find_moment_at(timestep)
        if moment:
            return moment
        old_moment = self._find_moment_before(timestep)
        new_moment = old_moment._clone(timestep)
        self.moments[timestep] = new_moment
        self.timesteps.insert(
            self.timesteps.index(old_moment.timestep) + 1,
            timestep,
            )
        return new_moment

    def add_group(self, add_action=None):
        self.root_node.add_group(add_action=add_action)

    def add_synth(self, duration=None, add_action=None):
        self.root_node.add_synth(duration=duration, add_action=add_action)

    def move_node(self, node, add_action=None):
        self.root_node.move_node(node, add_action=add_action)
