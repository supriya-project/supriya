# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class NRTSession(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_bus_counter',
        '_buses',
        '_control_bus_counter',
        '_node_counter',
        '_nodes',
        '_time_slices',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._audio_bus_counter = 0
        self._control_bus_counter = 0
        self._node_counter = 0
        self._buses = {}
        self._nodes = {}
        self._time_slices = []
        self._find_or_create_timeslice(0)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        from supriya.tools import nrttools
        if hasattr(expr, 'session_object'):
            expr = expr.session_object
        if isinstance(expr, (nrttools.NRTGroup, nrttools.NRTSynth)):
            return expr.nrt_id in self._nodes
        elif isinstance(expr, nrttools.NRTBus):
            return (expr.kind, expr.nrt_id) in self._buses
        return False

    ### PRIVATE METHODS ###

    def _find_or_create_timeslice(self, timestep):
        from supriya.tools import nrttools
        return nrttools.NRTTimeSlice(self, timestep)

    ### PUBLIC METHODS ###

    def at(self, timestep):
        return self._find_or_create_timeslice(timestep)

    def get_bus(self, kind='control'):
        from supriya.tools import nrttools
        assert kind in ('control', 'audio')
        if kind == 'audio':
            self._audio_bus_counter += 1
            nrt_id = self._audio_bus_counter
        else:
            self._control_bus_counter += 1
            nrt_id = self._control_bus_counter
        bus = nrttools.NRTBus(
            nrt_id=nrt_id,
            nrt_session=self,
            kind=kind,
            )
        self._buses[(bus.kind, bus.nrt_id)] = bus
        return bus

    def get_group(self):
        from supriya.tools import nrttools
        self._node_counter += 1
        group = nrttools.NRTGroup(
            nrt_id=self.node_counter,
            nrt_session=self,
            )
        self._nodes[group.nrt_id] = group
        return group

    def get_synth(self, synthdef, **kwargs):
        from supriya.tools import nrttools
        self._node_counter += 1
        synth = nrttools.NRTSynth(
            nrt_id=self.node_counter,
            nrt_session=self,
            synthdef=synthdef,
            **kwargs
            )
        self._nodes[synth.nrt_id] = synth
        return synth
