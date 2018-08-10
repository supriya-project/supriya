import re
import supriya.osc
import supriya.realtime
import supriya.system
from supriya.live.Track import Track
from supriya.system.Bindable import Bindable


class Mixer:

    ### INITIALIZER ###

    def __init__(self, channel_count=2, cue_channel_count=2):
        self._is_allowing_multiple = False
        channel_count = int(channel_count)
        cue_channel_count = int(cue_channel_count)
        assert self._is_power_of_two(channel_count)
        self._channel_count = channel_count
        assert self._is_power_of_two(cue_channel_count)
        assert cue_channel_count <= channel_count
        self._cue_channel_count = cue_channel_count
        self._levels_mapping = {}
        self._tracks = []
        self._tracks_by_name = {}
        self._group = supriya.realtime.Group()
        self._track_group = supriya.realtime.Group()
        self._server = None
        self._setup_cue_track()
        self._setup_master_track()

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._tracks_by_name[item]
        return self._tracks[item]

    def __iter__(self):
        for track in self._tracks:
            yield track.name
        yield 'master'
        yield 'cue'

    def __len__(self):
        return len(self._tracks_by_name)

    ### PRIVATE METHODS ###

    def _handle_input_levels(self, message):
        node_id = message.contents[0]
        levels = message.contents[2:]
        track = self._levels_mapping.get(node_id)
        if track is None:
            return
        peak, rms, = [], []
        for index in range(0, len(levels), 2):
            peak.append(levels[index])
            rms.append(levels[index + 1])
        levels = dict(peak=tuple(peak), rms=tuple(rms))
        track._input_levels = levels

    def _handle_prefader_levels(self, message):
        node_id = message.contents[0]
        levels = message.contents[2:]
        track = self._levels_mapping.get(node_id)
        if track is None:
            return
        peak, rms, = [], []
        for index in range(0, len(levels), 2):
            peak.append(levels[index])
            rms.append(levels[index + 1])
        levels = dict(peak=tuple(peak), rms=tuple(rms))
        track._prefader_levels = levels

    def _handle_postfader_levels(self, message):
        node_id = message.contents[0]
        levels = message.contents[2:]
        track = self._levels_mapping.get(node_id)
        if track is None:
            return
        peak, rms, = [], []
        for index in range(0, len(levels), 2):
            peak.append(levels[index])
            rms.append(levels[index + 1])
        levels = dict(peak=tuple(peak), rms=tuple(rms))
        track._postfader_levels = levels

    @staticmethod
    def _is_power_of_two(integer):
        integer = int(integer)
        if 0 < integer:
            return not bool(integer & (integer - 1))
        return False

    def _setup_master_track(self):
        track = Track(
            self,
            name='master',
            channel_count=self._channel_count,
            )
        mapping = [(i, i) for i in range(self._channel_count)]
        track.add_direct_out(mapping)
        self._tracks_by_name['master'] = track
        self._master_track = track

    def _setup_cue_track(self):
        track = Track(
            self,
            name='cue',
            channel_count=self.cue_channel_count,
            )
        offset = self._channel_count
        mapping = [(i, i + offset) for i in range(self.cue_channel_count)]
        track.add_direct_out(mapping)
        self._tracks_by_name['cue'] = track
        self._cue_track = track

    def _allocate_osc_callbacks(self):
        self._callbacks = [
            self.server.osc_io.register(
                pattern='/levels/input',
                procedure=self._handle_input_levels,
                ),
            self.server.osc_io.register(
                pattern='/levels/prefader',
                procedure=self._handle_prefader_levels,
                ),
            self.server.osc_io.register(
                pattern='/levels/postfader',
                procedure=self._handle_postfader_levels,
                ),
            ]

    def _free_osc_callbacks(self):
        for callback in self._callbacks:
            self.server.osc_io.unregister(callback)

    def _update_track_audibility(self):
        soloed_tracks = []
        for track in self.tracks:
            if track.is_soloed:
                soloed_tracks.append(track)
        if soloed_tracks:
            for track in self.tracks:
                if track in soloed_tracks:
                    track.output_synth.unpause()
                    track.output_synth['active'] = True
                else:
                    track.output_synth['active'] = False
        else:
            for track in self.tracks:
                track.output_synth['active'] = not track.is_muted

    ### PUBLIC METHODS ###

    def add_track(self, name, channel_count=None, index=None):
        assert name not in self._tracks_by_name
        track = Track(self, name=name, channel_count=channel_count)
        if index is None:
            self._tracks.append(track)
        else:
            assert 0 <= index < len(self._tracks)
            self._tracks.insert(index, track)
        self._tracks_by_name[name] = track
        if self.is_allocated:
            track._allocate_buses()
            track._allocate_nodes(self._track_group, index)
        track.send('master', 0.0)
        return track

    def allocate(self, server=None):
        server = server or supriya.realtime.Server.get_default_server()
        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        assert self.channel_count + 2 <= len(server.audio_output_bus_group)
        self._server = server
        self.group.allocate(target_node=self._server)
        self.group.append(self._track_group)
        self.master_track._allocate_buses()
        self.cue_track._allocate_buses()
        self._master_track._allocate_nodes(self._group)
        self._cue_track._allocate_nodes(self._group)
        for track in self._tracks:
            track._allocate_buses()
        for track in self._tracks:
            track._allocate_nodes(self._track_group)
        self.server.sync()
        self._update_track_audibility()
        self._allocate_osc_callbacks()
        return self

    def free(self):
        self._free_osc_callbacks()
        self._cue_track._free()
        self._master_track._free()
        for track in self._tracks:
            track._free()
        self._group.free()
        return self

    def lookup(self, name):
        current_object = self
        match = re.match(r'^(\w+)$', name)
        if match:
            name = match.group()
            if name.isdigit():
                name = int(name)
            try:
                return current_object[name]
            except (IndexError, KeyError):
                return getattr(current_object, name)
        match = re.match(r'^(\w+)([:.][\w]+)*', name)
        if not match:
            raise KeyError
        group = match.groups()[0]
        current_object = current_object[group]
        name = name[len(group):]
        for substring in re.findall('([:.][\\w]+)', name):
            operator, name = substring[0], substring[1:]
            if name.isdigit():
                name = int(name)
            if operator == ':':
                current_object = current_object[name]
            elif operator == '.':
                current_object = getattr(current_object, name)
        return current_object

    def remove_track(self, name):
        assert name in self._tracks_by_name
        track = self._tracks_by_name.pop(name)
        self._tracks.remove(track)
        if self.is_allocated:
            for target_name in tuple(track._outgoing_sends.keys()):
                track.remove_send(target_name)
            for source_name in tuple(track._incoming_sends.keys()):
                self._tracks_by_name[source_name].remove_send(name)
            track._free()
        track._mixer = None

    ### BINDABLES ###

    @Bindable(rebroadcast=True)
    def allow_multiple(self, state):
        self._is_allowing_multiple = bool(state)
        return self._is_allowing_multiple

    ### PUBLIC PROPERTIES ###

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def cue_channel_count(self):
        return self._cue_channel_count

    @property
    def cue_track(self):
        return self._cue_track

    @property
    def group(self):
        return self._group

    @property
    def is_allocated(self):
        return self._group.is_allocated

    @property
    def is_allowing_multiple(self):
        return self._is_allowing_multiple

    @property
    def master_track(self):
        return self._master_track

    @property
    def server(self):
        return self._server

    @property
    def tracks(self):
        return self._tracks

    @property
    def track_group(self):
        return self._track_group
