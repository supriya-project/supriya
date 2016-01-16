# -*- encoding: utf-8 -*-
import bisect


class NRTSession(object):

    ### INITIALIZER ###

    def __init__(self):
        from supriya.tools import nonrealtimetools
        self.nodes = set()
        self.active_moments = []
        self.timesteps = []
        self.moments = {}
        self.root_node = nonrealtimetools.NRTRootNode(self)
        self._setup_initial_moments()

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

    def _setup_initial_moments(self):
        from supriya.tools import nonrealtimetools
        timestep = float('-inf')
        moment = nonrealtimetools.NRTMoment(self, timestep)
        moment.nodes_to_children[self.root_node] = None
        moment.nodes_to_parent[self.root_node] = None
        self.moments[timestep] = moment
        self.timesteps.append(timestep)
        timestep = 0
        moment = moment._clone(timestep)
        self.moments[timestep] = moment
        self.timesteps.append(timestep)

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
        return self.root_node.add_group(add_action=add_action)

    def add_synth(self, duration=None, add_action=None):
        return self.root_node.add_synth(duration=duration, add_action=add_action)

    def move_node(self, node, add_action=None):
        self.root_node.move_node(node, add_action=add_action)

    def report(self):
        states = []
        for timestep in self.timesteps[1:]:
            moment = self.moments[timestep]
            state = moment.report()
            states.append(state)
        return states

#    def to_osc_bundles(self, timespan=None):
#        osc_bundles = []
#        visited_synthdefs = set()
#        for timestep in self.timesteps[1:]:
#            moment = self.moments[timestep]
#            requests = []
#            synthdefs = moment.synthdefs
#            visited_synthdefs.update(synthdefs)
