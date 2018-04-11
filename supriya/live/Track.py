import supriya.realtime
import supriya.synthdefs
import supriya.system
import supriya.ugens
from supriya.live.AutoPatternSlot import AutoPatternSlot
from supriya.live.Direct import Direct
from supriya.live.Send import Send
from supriya.live.SendManager import SendManager
from supriya.live.SynthSlot import SynthSlot
from supriya.live.TriggerPatternSlot import TriggerPatternSlot


class Track:

    ### INITIALIZER ###

    def __init__(
        self,
        mixer,
        name,
        channel_count=None,
        ):
        import supriya.live
        assert isinstance(mixer, supriya.live.Mixer)
        self._mixer = mixer
        channel_count = int(channel_count or self.mixer.channel_count)
        assert self._mixer._is_power_of_two(channel_count)
        self._channel_count = channel_count

        self._input_bus_group = supriya.realtime.BusGroup(
            bus_count=self._channel_count,
            calculation_rate='audio',
            )
        self._output_bus_group = supriya.realtime.BusGroup(
            bus_count=self._channel_count,
            calculation_rate='audio',
            )

        self._gain = float('-inf')
        self._is_cued = False
        self._is_muted = False
        self._is_soloed = False
        self._name = name
        self._incoming_sends = {}
        self._outgoing_sends = {}
        self._input_levels = None
        self._prefader_levels = None
        self._postfader_levels = None
        self._slots = []
        self._slots_by_name = {}

        self._group = supriya.realtime.Group(name=name)
        self._input_synth = supriya.realtime.Synth(
            synthdef=self.build_input_synthdef(self.channel_count))
        self._instrument_group = supriya.realtime.Group()
        self._send_group = supriya.realtime.Group()
        self._cue_synth = None
        self._direct_in = None
        self._direct_out = None
        if self.name != 'cue':
            self._cue_synth = supriya.realtime.Synth(
                synthdef=supriya.live.Send.build_synthdef(
                    self.channel_count, self.mixer.cue_track.channel_count),
                active=False,
                )
        self._output_synth = supriya.realtime.Synth(
            synthdef=self.build_output_synthdef(self.channel_count),
            gain=-96,
            )
        nodes = [_ for _ in [
            self._input_synth,
            self._instrument_group,
            self._cue_synth,
            self._output_synth,
            self._send_group,
            ] if _ is not None]
        self._group.extend(nodes)

    ### SPECIAL METHODS ###

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._slots[key]
        return self._slots_by_name[key]

    def __len__(self):
        return len(self._slots)

    def __iter__(self):
        for slot in self._slots:
            yield slot.name

    ### PRIVATE METHODS ###

    def _add_slot(self, slot):
        if slot.name in self._slots_by_name:
            raise ValueError
        self._slots.append(slot)
        self._slots_by_name[slot.name] = slot
        if self.is_allocated:
            slot._allocate()
        return slot

    def _allocate_buses(self):
        self.input_bus_group.allocate()
        self.output_bus_group.allocate()

    def _allocate_nodes(self, target_group, index=None):
        self.input_synth['in_'] = self.input_bus_group
        self.input_synth['out'] = self.output_bus_group
        self.output_synth['out'] = self.output_bus_group
        if self.cue_synth:
            self.cue_synth['in_'] = self.output_bus_group
            self.cue_synth['out'] = self.mixer.cue_track.input_bus_group
        if index is None:
            target_group.append(self._group)
        else:
            assert 0 <= index < len(target_group)
            target_group.insert(index, self.group)
        for send in self._outgoing_sends.values():
            send._allocate()
        self.mixer._levels_mapping[self.input_synth.node_id] = self
        self.mixer._levels_mapping[self.output_synth.node_id] = self
        for slot in self._slots:
            slot._allocate()
        if self.direct_in is not None:
            self.direct_in._allocate()
        if self.direct_out is not None:
            self.direct_out._allocate()

    def _as_node_target(self):
        return self.instrument_group

    def _free(self):
        for slot in self._slots:
            slot._free()
        if self.cue_synth:
            self.cue_synth.release()
        for send in tuple(self._incoming_sends.values()):
            send._free()
        for send in tuple(self._outgoing_sends.values()):
            send._free()
        self.group.free()
        self.output_bus_group.free()
        self.input_bus_group.free()

    def _handle_mute_and_solo(self):
        pass

    ### PUBLIC METHODS ###

    def add_auto_pattern_slot(self, name, pattern=None, synthdef=None, **kwargs):
        slot = AutoPatternSlot(
            name=name,
            track=self,
            synthdef=synthdef,
            pattern=pattern,
            **kwargs
            )
        return self._add_slot(slot)

    def add_direct_in(self, mapping):
        if not mapping:
            self.remove_direct_in()
            return
        direct_in = Direct(self, mapping, is_input=True)
        if self.direct_in is not None:
            self.direct_in._free()
        self._direct_in = direct_in
        if self.is_allocated:
            self._direct_in._allocate()

    def add_direct_out(self, mapping):
        if not mapping:
            self.remove_direct_out()
            return
        direct_out = Direct(self, mapping, is_input=False)
        if self.direct_out is not None:
            self.direct_out._free()
        self._direct_out = direct_out
        if self.is_allocated:
            self._direct_out._allocate()

    def remove_direct_in(self):
        if self.direct_in is None:
            return
        self.direct_in._free()
        self._direct_in = None

    def remove_direct_out(self):
        if self.direct_out is None:
            return
        self.direct_out._free()
        self._direct_out = None

    def add_send(self, target_name, initial_gain=0.0):
        assert target_name not in self._outgoing_sends
        source_track = self
        target_track = self.mixer[target_name]
        send = Send(
            source_track,
            target_track,
            initial_gain=initial_gain,
            )
        source_track._outgoing_sends[target_name] = send
        target_track._incoming_sends[source_track.name] = send
        if self.mixer.is_allocated:
            send._allocate()
        return send

    def add_synth_slot(self, name, synthdef=None, **kwargs):
        slot = SynthSlot(
            name=name,
            track=self,
            synthdef=synthdef,
            **kwargs
            )
        return self._add_slot(slot)

    def add_trigger_pattern_slot(self, name, pattern=None, synthdef=None, **kwargs):
        slot = TriggerPatternSlot(
            name=name,
            track=self,
            synthdef=synthdef,
            pattern=pattern,
            **kwargs
            )
        return self._add_slot(slot)

    @staticmethod
    def build_input_synthdef(channel_count):
        synthdef_builder = supriya.synthdefs.SynthDefBuilder(
            active=1,
            gain=0,
            gate=1,
            in_=supriya.synthdefs.Parameter(value=0, parameter_rate='scalar'),
            lag=0.1,
            out=supriya.synthdefs.Parameter(value=0, parameter_rate='scalar'),
            )
        with synthdef_builder:
            source = supriya.ugens.InFeedback.ar(
                bus=synthdef_builder['in_'],
                channel_count=channel_count,
                )
            supriya.ugens.SendPeakRMS.ar(
                command_name='/levels/input',
                source=source,
                )
            gate = supriya.ugens.Linen.kr(
                attack_time=synthdef_builder['lag'],
                done_action=supriya.synthdefs.DoneAction.FREE_SYNTH,
                gate=synthdef_builder['gate'],
                release_time=synthdef_builder['lag'],
                )
            active = supriya.ugens.Linen.kr(
                attack_time=synthdef_builder['lag'],
                done_action=supriya.synthdefs.DoneAction.NOTHING,
                gate=synthdef_builder['active'],
                release_time=synthdef_builder['lag'],
                )
            amplitude = (
                synthdef_builder['gain'].db_to_amplitude() *
                (synthdef_builder['gain'] > -96.0)
                ).lag(synthdef_builder['lag'])
            total_gain = gate * active * amplitude
            source *= total_gain
            supriya.ugens.ReplaceOut.ar(
                bus=synthdef_builder['out'],
                source=source,
                )
        name = 'mixer/input/{}'.format(channel_count)
        return synthdef_builder.build(name=name)

    @staticmethod
    def build_output_synthdef(channel_count):
        synthdef_builder = supriya.synthdefs.SynthDefBuilder(
            active=1,
            gain=0,
            gate=1,
            lag=0.1,
            out=supriya.synthdefs.Parameter(value=0, parameter_rate='scalar'),
            )
        with synthdef_builder:
            source = supriya.ugens.In.ar(
                bus=synthdef_builder['out'],
                channel_count=channel_count,
                )
            supriya.ugens.SendPeakRMS.ar(
                command_name='/levels/prefader',
                source=source,
                )
            gate = supriya.ugens.Linen.kr(
                attack_time=synthdef_builder['lag'],
                done_action=supriya.synthdefs.DoneAction.FREE_SYNTH,
                gate=synthdef_builder['gate'],
                release_time=synthdef_builder['lag'],
                )
            active = supriya.ugens.Linen.kr(
                attack_time=synthdef_builder['lag'],
                done_action=supriya.synthdefs.DoneAction.NOTHING,
                gate=synthdef_builder['active'],
                release_time=synthdef_builder['lag'],
                )
            amplitude = (
                synthdef_builder['gain'].db_to_amplitude() *
                (synthdef_builder['gain'] > -96.0)
                ).lag(synthdef_builder['lag'])
            total_gain = gate * active * amplitude
            source *= total_gain
            supriya.ugens.SendPeakRMS.ar(
                command_name='/levels/postfader',
                source=source,
                )
            supriya.ugens.ReplaceOut.ar(
                bus=synthdef_builder['out'],
                source=source,
                )
        name = 'mixer/output/{}'.format(channel_count)
        return synthdef_builder.build(name=name)

    def remove_send(self, target_name):
        assert target_name in self._outgoing_sends
        send = self._outgoing_sends.pop(target_name)
        target_track = self.mixer[target_name]
        target_track._incoming_sends.pop(self.name)
        send._free()
        self._track = None

    ### BINDABLES ###

    def get_cue(self):
        return self.is_cued

    def get_gain(self):
        return self.gain

    def get_mute(self):
        return self.is_muted

    def get_solo(self):
        return self.is_soloed

    @supriya.system.Bindable(rebroadcast=True)
    def set_cue(self, state):
        if self.name == 'cue':
            return False
        elif not state:
            self._is_cued = False
            self.cue_synth['active'] = False
        else:
            self._is_cued = True
            self.cue_synth['active'] = True
            if not self.mixer.is_allowing_multiple:
                for track in self.mixer.tracks + [self.mixer.master_track]:
                    if track is self:
                        continue
                    elif track.is_cued:
                        track.set_cue(False)
        return state

    @supriya.system.Bindable(rebroadcast=True)
    def set_gain(self, gain):
        self._gain = gain
        self.output_synth['gain'] = gain
        return gain

    @supriya.system.Bindable(rebroadcast=True)
    def set_mute(self, state):
        if self.name in ('master',):
            return False
        if state:
            self._is_muted = True
            self._is_soloed = False
        else:
            self._is_muted = False
        self.mixer._update_track_audibility()
        return bool(state)

    @supriya.system.Bindable(rebroadcast=True)
    def set_solo(self, state, handle=True):
        if self.name in ('cue', 'master'):
            return False
        if state:
            self._is_muted = False
            self._is_soloed = True
            if not self.mixer.is_allowing_multiple:
                for track in self.mixer.tracks:
                    if track is self:
                        continue
                    track.set_solo(False, handle=False)
        else:
            self._is_soloed = False
        if handle:
            self.mixer._update_track_audibility()
        return bool(state)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def cue_synth(self):
        return self._cue_synth

    @property
    def direct_in(self):
        return self._direct_in

    @property
    def direct_out(self):
        return self._direct_out

    @property
    def gain(self):
        return self._gain

    @property
    def group(self):
        return self._group

    @property
    def input_bus_group(self):
        return self._input_bus_group

    @property
    def input_synth(self):
        return self._input_synth

    @property
    def instrument_group(self):
        return self._instrument_group

    @property
    def is_allocated(self):
        return self._group.is_allocated

    @property
    def is_cued(self):
        return self._is_cued

    @property
    def is_muted(self):
        return self._is_muted

    @property
    def is_soloed(self):
        return self._is_soloed

    @property
    def mixer(self):
        return self._mixer

    @property
    def name(self):
        return self._name

    @property
    def output_bus_group(self):
        return self._output_bus_group

    @property
    def output_synth(self):
        return self._output_synth

    @property
    def send(self):
        return SendManager(self)

    @property
    def send_group(self):
        return self._send_group

    @property
    def input_levels(self):
        return self._input_levels

    @property
    def prefader_levels(self):
        return self._prefader_levels

    @property
    def postfader_levels(self):
        return self._postfader_levels

    @property
    def synth_kwargs(self):
        return dict(
            target_node=self,
            in_=int(self.output_bus_group),
            out=int(self.output_bus_group),
            )
