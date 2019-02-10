import supriya.realtime
import supriya.synthdefs
import supriya.ugens


class Direct:

    ### INITIALIZER ###

    def __init__(self, track, mapping=None, is_input=False):
        self._track = track
        self._is_input = bool(is_input)
        self._mapping = tuple(sorted(mapping))
        self._synth = None

    ### PRIVATE METHODS ###

    def _allocate(self):
        if self.is_input:
            source_track_count = len(self.mixer.server.audio_input_bus_group)
            target_track_count = self.track.channel_count
        else:
            source_track_count = self.track.channel_count
            target_track_count = len(self.mixer.server.audio_output_bus_group)
        synthdef = self.build_synthdef(
            source_track_count, target_track_count, self.mapping
        )
        self._synth = supriya.realtime.Synth(synthdef=synthdef)
        if self.is_input:
            in_ = int(self.mixer.server.audio_input_bus_group)
            out = int(self.track.input_bus_group)
        else:
            in_ = int(self.track.output_bus_group)
            out = int(self.mixer.server.audio_output_bus_group)
        self.synth["in_"] = in_
        self.synth["out"] = out
        if self.is_input:
            self.track.group.insert(0, self.synth)
        else:
            self.track.group.append(self.synth)

    def _free(self):
        if self.synth is not None:
            self.synth.release()
        self._synth = None

    ### PUBLIC METHODS ###

    @staticmethod
    def build_synthdef(source_track_count, target_track_count, mapping):
        for in_, out in mapping:
            assert 0 <= in_ < source_track_count
            assert 0 <= out < target_track_count
        synthdef_builder = supriya.synthdefs.SynthDefBuilder(
            gate=1,
            lag=0.1,
            in_=supriya.synthdefs.Parameter(value=0, parameter_rate="scalar"),
            out=supriya.synthdefs.Parameter(value=0, parameter_rate="scalar"),
        )
        with synthdef_builder:
            source = supriya.ugens.In.ar(
                bus=synthdef_builder["in_"], channel_count=source_track_count
            )
            gate = supriya.ugens.Linen.kr(
                attack_time=synthdef_builder["lag"],
                done_action=supriya.DoneAction.FREE_SYNTH,
                gate=synthdef_builder["gate"],
                release_time=synthdef_builder["lag"],
            )
            source *= gate
            zero = supriya.ugens.DC.ar(0)
            mapped = []
            for _ in range(target_track_count):
                mapped.append([])
            for in_, out in mapping:
                mapped[out].append(source[in_])
            for i, out in enumerate(mapped):
                if not out:
                    out.append(zero)
                mapped[i] = supriya.ugens.Mix.new(out)
            supriya.ugens.Out.ar(bus=synthdef_builder["out"], source=mapped)
        name = "mixer/direct/{}".format(
            ",".join("{}:{}".format(in_, out) for in_, out in mapping)
        )
        return synthdef_builder.build(name=name)

    ### PUBLIC PROPERTIES ###

    @property
    def is_allocated(self):
        return self.synth.is_allocated

    @property
    def is_input(self):
        return self._is_input

    @property
    def mapping(self):
        return self._mapping

    @property
    def mixer(self):
        return self.track.mixer

    @property
    def synth(self):
        return self._synth

    @property
    def track(self):
        return self._track
