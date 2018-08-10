import supriya.realtime
import supriya.synthdefs
import supriya.system
import supriya.ugens
from supriya.system.Bindable import Bindable


class Send:

    ### INITIALIZER ###

    def __init__(self, source_track, target_track, initial_gain=0.):
        self._source_track = source_track
        self._target_track = target_track
        self._gain = float(initial_gain)
        synthdef = self.build_synthdef(
            self.source_track_count,
            self.target_track_count,
            )
        self._synth = supriya.realtime.Synth(
            synthdef=synthdef,
            gain=self.gain,
            in_=0,
            out=0,
            )

    ### SPECIAL METHODS ###

    @Bindable
    def __call__(self, gain):
        self._gain = float(gain)
        if self.synth and self.synth.is_allocated:
            self.synth['gain'] = self.gain
        return gain

    ### PRIVATE METHODS ###

    def _allocate(self):
        self.synth['in_'] = self.source_track.output_bus_group
        self.synth['out'] = self.target_track.input_bus_group
        self.synth['gain'] = self.gain
        self.source_track.send_group.append(self.synth)

    def _free(self):
        self._synth.release()

    ### PUBLIC METHODS ###

    @staticmethod
    def build_synthdef(source_track_count, target_track_count):
        synthdef_builder = supriya.synthdefs.SynthDefBuilder(
            active=1,
            gain=0,
            gate=1,
            in_=supriya.synthdefs.Parameter(value=0, parameter_rate='scalar'),
            lag=0.1,
            out=supriya.synthdefs.Parameter(value=0, parameter_rate='scalar'),
            )
        with synthdef_builder:
            source = supriya.ugens.In.ar(
                bus=synthdef_builder['in_'],
                channel_count=source_track_count,
                )
            mix_factor = source_track_count / target_track_count
            if source_track_count == target_track_count:
                pass
            elif target_track_count == 1:
                source = supriya.ugens.Mix.new(source) / mix_factor
            elif source_track_count == 1:
                source = supriya.synthdefs.UGenArray([source] * target_track_count)
            else:
                panners = []
                for i, channel in enumerate(source):
                    position = (-1 / len(source)) + ((2 / len(source)) * i)
                    amplitude = 1
                    width = 2 * (1 / mix_factor)
                    if mix_factor > 1:
                        amplitude = 1 / mix_factor
                    panner = supriya.ugens.PanAz.ar(
                        channel_count=target_track_count,
                        source=channel,
                        position=position,
                        amplitude=amplitude,
                        width=width,
                        )
                    panners.extend(panner)
                source = supriya.ugens.Mix.multichannel(
                    panners,
                    target_track_count,
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
            supriya.ugens.Out.ar(
                bus=synthdef_builder['out'],
                source=source,
                )
        name = 'mixer/send/{}x{}'.format(
            source_track_count,
            target_track_count,
            )
        return synthdef_builder.build(name=name)

    ### PUBLIC PROPERTIES ###

    @property
    def gain(self):
        return self._gain

    @property
    def is_allocated(self):
        return self.synth.is_allocated

    @property
    def mixer(self):
        return self._source_track.mixer

    @property
    def source_track(self):
        return self._source_track

    @property
    def source_track_count(self):
        return self._source_track.channel_count

    @property
    def synth(self):
        return self._synth

    @property
    def target_track(self):
        return self._target_track

    @property
    def target_track_count(self):
        return self._target_track.channel_count
