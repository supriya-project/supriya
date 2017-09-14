from supriya.tools import servertools
from supriya.tools import ugentools
from supriya.tools import synthdeftools


class Direct:

    ### INITIALIZER ###

    def __init__(self, track, mapping=None, is_input=False):
        self._is_input = bool(is_input)
        self._mapping = tuple(sorted((mapping or {}).items()))
        if self.is_input:
            source_track_count = len(self.mixer.server.audio_input_bus_group)
            target_track_count = self.track.channel_count
        else:
            source_track_count = self.track.channel_count
            target_track_count = len(self.mixer.server.audio_output_bus_group)
        synthdef = self.build_synthdef(
            source_track_count,
            target_track_count,
            self.mapping,
            )
        self._synth = servertools.Synth(synthdef=synthdef)
        self._track = track

    ### PRIVATE METHODS ###

    def _allocate(self):
        if self.is_input:
            in_ = int(self.mixer.server.audio_input_bus_group)
            out = int(self.track.input_bus_group)
        else:
            in_ = int(self.track.output_bus_group)
            out = int(self.mixer.server.audio_output_bus_group)
        self.synth['in_'] = in_
        self.synth['out'] = out
        if self.is_input:
            self.track.group.append(self.synth)
        else:
            self.track.group.insert(0, self.synth)

    def _free(self):
        self.synth.release()

    ### PUBLIC METHODS ###

    @staticmethod
    def build_synthdef(
        source_track_count,
        target_track_count,
        mapping,
        ):
        if isinstance(mapping, dict):
            mapping = sorted(mapping.items())
        for in_, out in mapping:
            assert 0 <= in_ < source_track_count
            assert 0 <= out < target_track_count
        synthdef_builder = synthdeftools.SynthDefBuilder(
            gate=1,
            in_=synthdeftools.Parameter(value=0, parameter_rate='scalar'),
            out=synthdeftools.Parameter(value=0, parameter_rate='scalar'),
            )
        with synthdef_builder:
            source = ugentools.In.ar(
                bus=synthdef_builder['in_'],
                channel_count=source_track_count,
                )
            zero = ugentools.DC.ar()
            mapped = [[]] * target_track_count
            for in_, out in mapping:
                in_ = source[in_]
                out = mapped[out]
                out.append(in_)
            for i, out in enumerate(mapped):
                if not out:
                    out.append(zero)
                mapped[i] = ugentools.Mix.new(out)
            ugentools.Out.ar(
                bus=synthdef_builder['out'],
                source=mapped,
                )
        name = 'mixer/send/{}'.format(
            '/'.join(
                '{}x{}'.format(in_, out)
                for in_, out in sorted(mapping.items()),
            ))
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
