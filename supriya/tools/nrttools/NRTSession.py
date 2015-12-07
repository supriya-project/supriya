# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class NRTSession(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_buses',
        '_control_buses',
        '_nodes',
        '_time_slices',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._audio_bus_counter = 0
        self._audio_buses = {}
        self._control_bus_counter = 0
        self._control_buses = {}
        self._node_counter = 0
        self._nodes = {}
        self._time_slices = {}

    ### PUBLIC METHODS ###

    def get_group(self):
        from supriya.tools import nrttools
        self._node_counter += 1
        group = nrttools.NRTGroup(
            nrt_id=self.node_counter,
            nrt_session=self,
            )
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
        return synth

    def get_bus(self, kind='control'):
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
        return bus
