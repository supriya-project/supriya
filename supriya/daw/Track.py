from uqbar.containers import UniqueTreeTuple
from uqbar.strings import delimit_words

from supriya.daw.synthdefs import (
    build_track_input_synthdef,
    build_track_output_synthdef,
)
from supriya.realtime import BusGroup, Group, Synth

from .ClipSlotContainer import ClipSlotContainer
from .DawNode import DawNode
from .DeviceContainer import DeviceContainer
from .DeviceType import DeviceType
from .Send import Send
from .SendManager import SendManager
from .TrackReceive import TrackReceive


class Track(DawNode, UniqueTreeTuple):

    ### INITIALIZER ###

    def __init__(self, *, device_types=None, channel_count=2, name=None):
        DawNode.__init__(self)
        self._device_types = device_types or (
            DeviceType.MIDI,
            DeviceType.INSTRUMENT,
            DeviceType.AUDIO,
        )

        self._bus_group = BusGroup.audio(bus_count=channel_count)
        self._devices = DeviceContainer(device_types=self.device_types)
        self._input_bus_group = BusGroup.audio(bus_count=channel_count)
        self._input_synth = Synth(synthdef=build_track_input_synthdef(channel_count))
        self._levels = dict(input=None, prefader=None, postfader=None)
        self._osc_callbacks = dict(input=None, prefader=None, postfader=None)
        self._output_synth = Synth(synthdef=build_track_output_synthdef(channel_count))
        self._receive = TrackReceive()
        self._sends = SendManager()
        self._slots = ClipSlotContainer()
        self._slots._parent = self

        self._is_active = True
        self._is_muted = False
        self._is_soloed = False
        self._soloed_tracks = set()

        UniqueTreeTuple.__init__(
            self, children=[self.receive, self.devices, self.sends]
        )

        self._node = Group(
            children=[
                self.input_synth,
                self.devices.node,
                self.sends.pre_fader_group,
                self.output_synth,
                self.sends.post_fader_group,
            ],
            name=name
            or " ".join(_.lower() for _ in delimit_words(type(self).__name__)),
        )

    ### PRIVATE METHODS ###

    def _create_bus_routings(self, server):
        self.input_synth["in_"] = self._input_bus_group
        self.input_synth["out"] = self._bus_group
        self.output_synth["out"] = self._bus_group

    def _create_osc_callbacks(self, server):
        def update_levels(key, levels):
            levels = list(levels)
            peak, rms = [], []
            while levels:
                peak.append(levels.pop(0))
                rms.append(levels.pop(0))
            self._levels[key] = peak, rms

        self._osc_callbacks["input"] = server.osc_io.register(
            ["/levels/track/input", self._input_synth.node_id],
            lambda osc_message: update_levels("input", osc_message.contents[2:]),
        )
        self._osc_callbacks["prefader"] = server.osc_io.register(
            ["/levels/track/prefader", self._output_synth.node_id],
            lambda osc_message: update_levels("prefader", osc_message.contents[2:]),
        )
        self._osc_callbacks["postfader"] = server.osc_io.register(
            ["/levels/track/postfader", self._output_synth.node_id],
            lambda osc_message: update_levels("postfader", osc_message.contents[2:]),
        )

    def _destroy_osc_callbacks(self, server):
        for key, callback in self._osc_callbacks.items():
            if callback and server:
                server.osc_io.unregister(callback)

    def _list_bus_groups(self):
        return [self.input_bus_group, self.bus_group]

    def _mute(self, muted):
        if muted and self.is_muted:
            return
        elif not muted and not self.is_muted:
            return
        self._is_muted = bool(muted)
        parentage_is_muted = False
        for parent in self.parentage[1:]:
            if isinstance(parent, Track) and parent.is_muted:
                parentage_is_muted = True
                break
        if parentage_is_muted:
            # muting or unmuting will not change anything
            return
        self._update_activation()

    def _set_parent(self, new_parent):
        for parent in self.parentage[:1]:
            parent._soloed_tracks.difference_update(self._soloed_tracks)
        DawNode._set_parent(self, new_parent)
        for parent in self.parentage[:1]:
            parent._soloed_tracks.update(self._soloed_tracks)

    def _update_activation(self):
        def recurse(track, tree_is_muted=False, tree_is_soloed=False):
            should_mute = bool(tree_is_muted or track.is_muted)
            should_solo = bool(tree_is_soloed or track._soloed_tracks)
            active = True
            if should_mute:
                active = False
            if any_tracks_are_soloed:
                active = should_solo
            if not track.is_active and active:
                track._debug_tree("Activating")
                to_activate.append(track)
            elif track.is_active and not active:
                track._debug_tree("De-activating")
                to_deactivate.append(track)
            if isinstance(track, GroupTrack):
                for child in track.tracks:
                    recurse(
                        child,
                        tree_is_muted=should_mute,
                        tree_is_soloed=tree_is_soloed or track.is_soloed,
                    )

        from .GroupTrack import GroupTrack
        from .TrackContainer import TrackContainer

        parentage = self.parentage
        root = parentage[-1]
        if parentage[-1] is self.application:
            root = parentage[-2]
        any_tracks_are_soloed = bool(root._soloed_tracks)
        to_activate, to_deactivate = [], []
        if isinstance(root, TrackContainer):
            for track in root:
                recurse(track)
        else:
            recurse(root)
        # TODO: Bundle requests here
        for track in to_activate:
            track._is_active = True
            track.output_synth["active"] = 1
            for send in track.sends._iter_children():
                if send.node:
                    send.node["active"] = 1
        for track in to_deactivate:
            track._is_active = False
            track.output_synth["active"] = 0
            for send in track.sends._iter_children():
                if send.node:
                    send.node["active"] = 0

    ### PUBLIC METHODS ###

    def add_clip_slot(self):
        pass

    def add_send(self, target, post_fader=True) -> Send:
        send = Send(self, target, post_fader=post_fader)
        self.sends[target] = send
        return send

    def delete(self):
        self.parent.remove(self)

    def mute(self):
        self._mute(True)

    @classmethod
    def perform(cls, *, device=None, moment=None, start_notes=None, stop_notes=None):
        stack = []
        if device and (start_notes or stop_notes):
            stack.append((device, start_notes, stop_notes))
        while stack:
            device, start_notes, stop_notes = stack.pop()
            result = device.peform()
            if result:
                start_notes, stop_notes = result
                for next_device in device.next_devices():
                    stack.append((next_device, start_notes, stop_notes))

    def solo(self, exclusive=True):
        if self.is_soloed:
            return
        self._debug_tree("Soloing...")
        parentage = self.parentage
        self._is_soloed = True
        if exclusive:
            for track in tuple(parentage[-1]._soloed_tracks):
                track._is_soloed = False
                for node in track.parentage:
                    node._soloed_tracks.remove(track)
        for node in parentage:
            node._soloed_tracks.add(self)
        self._update_activation()

    def unmute(self):
        self._mute(False)

    def unsolo(self):
        if not self.is_soloed:
            return
        self._debug_tree("Un-soloing...")
        self._is_soloed = False
        parentage = self.parentage
        for node in parentage:
            node._soloed_tracks.remove(self)
        self._update_activation()

    ### PUBLIC PROPERTIES ###

    @property
    def is_active(self):
        return self._is_active

    @property
    def bus_group(self) -> BusGroup:
        return self._bus_group

    @property
    def channel_count(self) -> int:
        return len(self._bus_group)

    @property
    def default_send_target(self):
        for parent in self.parentage[1:]:
            if hasattr(parent, "tracks"):
                if hasattr(parent, "master_track"):
                    return parent.master_track
                return parent

    @property
    def devices(self) -> DeviceContainer:
        return self._devices

    @property
    def device_types(self):
        return self._device_types

    @property
    def input_bus_group(self) -> BusGroup:
        return self._input_bus_group

    @property
    def input_synth(self) -> Synth:
        return self._input_synth

    @property
    def is_muted(self):
        return self._is_muted

    @property
    def is_soloed(self):
        return self._is_soloed

    @property
    def output_synth(self) -> Synth:
        return self._output_synth

    @property
    def parentage_is_muted(self):
        for parent in self.parentage:
            if isinstance(parent, type(self)) and parent.is_muted:
                return True
        return False

    @property
    def receive(self):
        return self._receive

    @property
    def sends(self):
        return self._sends

    @property
    def slots(self):
        return self._slots
