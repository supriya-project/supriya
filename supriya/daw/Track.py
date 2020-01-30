from typing import Optional

from uqbar.containers import UniqueTreeTuple
from uqbar.strings import delimit_words

from supriya.daw.synthdefs import (
    build_track_input_synthdef,
    build_track_output_synthdef,
)
from supriya.realtime import BusGroup, Group, Synth

from .Clip import Clip
from .ClipSlot import ClipSlot
from .ClipSlotContainer import ClipSlotContainer
from .DawNode import DawNode
from .Device import Device
from .DeviceContainer import DeviceContainer
from .DeviceType import DeviceType
from .DirectIn import DirectIn
from .DirectOut import DirectOut
from .Send import Send
from .SendContainer import SendContainer
from .TrackReceive import TrackReceive


class Track(DawNode, UniqueTreeTuple):

    ### INITIALIZER ###

    def __init__(self, *, device_types=None, channel_count=2, name=None):
        from .TrackContainer import TrackContainer

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
        self._output_synth = Synth(synthdef=build_track_output_synthdef(channel_count))
        self._receive = TrackReceive()
        self._sends = SendContainer()
        self._slots = ClipSlotContainer()
        self._slots._parent = self
        self._tracks = TrackContainer()

        self._levels = dict(input=None, prefader=None, postfader=None)
        self._osc_callbacks = dict(input=None, prefader=None, postfader=None)

        self._is_active = True
        self._is_monitoring_midi = False
        self._is_muted = False
        self._is_soloed = False
        self._soloed_tracks = set()

        self._active_slot_index: Optional[int] = None
        self._active_slot_start_delta: 0.0
        self._pending_slot_index: Optional[int] = None
        self._clip_launch_event_id: Optional[int] = None
        self._clip_perform_event_id: Optional[int] = None

        UniqueTreeTuple.__init__(
            self, children=[self.tracks, self.receive, self.devices, self.sends]
        )

        self._node = Group(
            children=[
                self.receive.node,
                self.input_synth,
                self.tracks.node,
                self.devices.node,
                self.sends.pre_fader_group,
                self.output_synth,
                self.sends.post_fader_group,
            ],
            name=name
            or " ".join(_.lower() for _ in delimit_words(type(self).__name__)),
        )

    ### PRIVATE METHODS ###

    def _clip_launch_callback(self, current_moment, desired_moment, event):
        with self.application._lock:
            # self._debug_tree("Clip Launch")
            self._clip_launch_event_id = None
            if self._active_slot_index is not None:
                clip = self.slots[self._active_slot_index].clip
                clip_moment = clip.at(
                    desired_moment.offset,
                    start_delta=self._active_slot_start_delta,
                    force_stop=True,
                )
                # self._debug_tree("Clip Launch (Stop)")
                self.perform(desired_moment, clip_moment.note_off_messages)
            # TODO: check if pending slot index is in bounds, do not proceed if not
            if self._pending_slot_index is not None and not (
                0 <= self._pending_slot_index < len(self.slots)
            ):
                self._active_slot_start_delta = None
                self._active_slot_index = None
                self._pending_slot_index = None
                return
            self._active_slot_index = self._pending_slot_index
            self._active_slot_start_delta = desired_moment.offset
            if self._active_slot_index is None:
                if self._clip_perform_event_id:
                    self.transport.clock.cancel(self._clip_perform_event_id)
                    self._clip_perform_event_id = None
                return
            if self._clip_perform_event_id:
                self.transport.clock.reschedule(
                    self._clip_perform_event_id, schedule_at=desired_moment.offset
                )
            else:
                self._clip_perform_event_id = self.transport.clock.schedule(
                    self._clip_perform_callback,
                    schedule_at=desired_moment.offset,
                    event_type=Clip.EventType.PERFORM,
                )

    def _clip_perform_callback(self, current_moment, desired_moment, event):
        with self.application._lock:
            clip = self.slots[self._active_slot_index].clip
            clip_moment = clip.at(
                desired_moment.offset, start_delta=self._active_slot_start_delta
            )
            # self._debug_tree("Clip Perform", suffix=repr(clip_moment))
            midi_messages = clip_moment.note_off_messages + clip_moment.note_on_messages
            self.perform(desired_moment, midi_messages)
            if clip_moment.next_offset is None:
                delta = None
            else:
                delta = clip_moment.next_offset - desired_moment.offset
            self._debug_tree("Clip Perform", suffix="Delta {}".format(delta))
            return delta

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

        self._osc_callbacks["input"] = server.osc_protocol.register(
            ["/levels/track/input", self._input_synth.node_id],
            lambda osc_message: update_levels("input", osc_message.contents[2:]),
        )
        self._osc_callbacks["prefader"] = server.osc_protocol.register(
            ["/levels/track/prefader", self._output_synth.node_id],
            lambda osc_message: update_levels("prefader", osc_message.contents[2:]),
        )
        self._osc_callbacks["postfader"] = server.osc_protocol.register(
            ["/levels/track/postfader", self._output_synth.node_id],
            lambda osc_message: update_levels("postfader", osc_message.contents[2:]),
        )

    def _destroy_osc_callbacks(self, server):
        for key, callback in self._osc_callbacks.items():
            if callback and server:
                server.osc_protocol.unregister(callback)

    def _list_bus_groups(self):
        return [self.input_bus_group, self.bus_group]

    def _mute(self, muted):
        with self.lock_applications((self,)):
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
            for child in track.tracks:
                recurse(
                    child,
                    tree_is_muted=should_mute,
                    tree_is_soloed=tree_is_soloed or track.is_soloed,
                )

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
        clip_slot = ClipSlot()
        self.slots.append(clip_slot)
        return clip_slot

    def add_direct_in(self, source_bus_id: int, source_bus_count: int) -> DirectIn:
        direct_in = DirectIn(
            source_bus_id=source_bus_id, source_bus_count=source_bus_count, target=self
        )
        self.receive.append(direct_in)
        return direct_in

    def add_direct_out(self, target_bus_id: int, target_bus_count: int) -> DirectOut:
        direct_out = DirectOut(
            source=self, target_bus_id=target_bus_id, target_bus_count=target_bus_count
        )
        self.sends.append(direct_out)
        return direct_out

    def add_send(self, target, post_fader=True) -> Send:
        send = Send(self, target, post_fader=post_fader)
        self.sends.append(send)
        return send

    def add_track(self, channel_count=2, name=None) -> "Track":
        track = Track(channel_count=channel_count, name=name)
        self.tracks.append(track)
        track.add_send(Send.DEFAULT)
        return track

    def delete(self):
        self.parent.remove(self)

    def fire_clip_slot(self, slot_index):
        self._pending_slot_index = slot_index
        transport = self.transport
        if transport is None:
            return
        transport.clock.cue(
            self._clip_launch_callback,
            quantization=transport.default_quantization,
            event_type=Clip.EventType.LAUNCH,
        )
        if not transport.is_running:
            transport.start()

    @classmethod
    def group(cls, tracks, name=None):
        # if not tracks:
        #    raise ValueError("No tracks to group")
        if not all(isinstance(track, Track) for track in tracks):
            raise ValueError("Cannot group non-tracks")
        # if len(set(track.application for track in tracks)) > 1:
        #    raise ValueError("All tracks must share same application")
        # if len(set(track.parent for track in tracks)) > 1:
        #    raise ValueError("All tracks must share same parent")
        with cls.lock_applications(tracks):
            group_track = cls(name=name)
            group_track._debug_tree("Grouping...")
            group_track.add_send(Send.DEFAULT)
            if tracks and tracks[0].parent is not None:
                index = tracks[0].parent.index(tracks[0])
                tracks[0].parent.insert(index, group_track)
            group_track.tracks.extend(tracks)
        return group_track

    def stop_clip(self):
        self._pending_slot_index = None
        transport = self.transport
        if transport is None:
            return
        transport.clock.cue(
            self._clip_launch_callback,
            quantization=transport.default_quantization,
            event_type=Clip.EventType.LAUNCH,
        )

    def monitor_midi(self, should_monitor=True):
        application = self.application
        if application is None:
            raise RuntimeError("No application to coordinate with")
        self._is_monitoring_midi = bool(should_monitor)
        if self._is_monitoring_midi:
            application._midi_monitoring_tracks.append(self)
        else:
            application._midi_monitoring_tracks.remove(self)

    def mute(self):
        self._mute(True)

    def perform(self, moment, in_midi_messages):
        if not self.devices:
            return
        requests = Device.perform_loop(
            moment, self.devices[0].perform, in_midi_messages
        )
        self.application.send_requests(moment, requests)

    def solo(self, exclusive=True):
        if self.is_soloed:
            return
        with self.lock_applications([self]):
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

    def ungroup(self) -> "Track":
        with self.lock_applications([self]):
            self._debug_tree("Ungrouping")
            if self.parent is None:
                raise ValueError("Cannot ungroup without parent")
            index = self.parent.index(self)
            self.parent[index:index] = self.tracks[:]
            self.parent.remove(self)
        return self

    def unmute(self):
        self._mute(False)

    def unsolo(self):
        if not self.is_soloed:
            return
        with self.lock_applications([self]):
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
    def is_monitoring_midi(self):
        return self._is_monitoring_midi

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

    @property
    def tracks(self):
        return self._tracks
