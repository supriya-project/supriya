from supriya.tools import servertools
from supriya.tools import synthdeftools
from supriya.tools import systemtools
from supriya.tools import ugentools


class Send:

    ### INITIALIZER ###

    def __init__(self, source_track, target_track, initial_gain=0.):
        self._source_track = source_track
        self._target_track = target_track
        self._gain = float(initial_gain)
        self._synth = None

    ### SPECIAL METHODS ###

    @systemtools.Bindable
    def __call__(self, gain):
        self._gain = float(gain)
        if self.synth and self.synth.is_allocated:
            self.synth['gain'] = self.gain
        return gain

    ### PRIVATE METHODS ###

    def _allocate(self):
        synthdef = self.build_synthdef(
            self.source_track_count,
            self.target_track_count,
            )
        self._synth = servertools.Synth(
            synthdef=synthdef,
            gain=self.gain,
            in_=self.source_track.output_bus_group,
            out=self.target_track.input_bus_group,
            )
        self.source_track.send_group.append(self._synth)

    def _free(self):
        self._synth.release()
        self._synth = None

    ### PUBLIC METHODS ###

    @staticmethod
    def build_synthdef(source_track_count, target_track_count):
        synthdef_builder = synthdeftools.SynthDefBuilder(
            active=1,
            gain=0,
            gate=1,
            in_=synthdeftools.Parameter(value=0, parameter_rate='scalar'),
            lag=0.1,
            out=synthdeftools.Parameter(value=0, parameter_rate='scalar'),
            )
        with synthdef_builder:
            source = ugentools.In.ar(
                bus=synthdef_builder['in_'],
                channel_count=source_track_count,
                )
            mix_factor = source_track_count / target_track_count
            if source_track_count == target_track_count:
                pass
            elif target_track_count == 1:
                source = ugentools.Mix.new(source) / mix_factor
            elif source_track_count == 1:
                source = synthdeftools.UGenArray([source] * target_track_count)
            else:
                panners = []
                for i, channel in enumerate(source):
                    position = (-1 / len(source)) + ((2 / len(source)) * i)
                    amplitude = 1
                    width = 2 * (1 / mix_factor)
                    if mix_factor > 1:
                        amplitude = 1 / mix_factor
                    panner = ugentools.PanAz.ar(
                        channel_count=target_track_count,
                        source=channel,
                        position=position,
                        amplitude=amplitude,
                        width=width,
                        )
                    panners.extend(panner)
                source = ugentools.Mix.multichannel(
                    panners,
                    target_track_count,
                    )
            gate = ugentools.Linen.kr(
                attack_time=synthdef_builder['lag'],
                done_action=synthdeftools.DoneAction.FREE_SYNTH,
                gate=synthdef_builder['gate'],
                release_time=synthdef_builder['lag'],
                )
            active = ugentools.Linen.kr(
                attack_time=synthdef_builder['lag'],
                done_action=synthdeftools.DoneAction.NOTHING,
                gate=synthdef_builder['active'],
                release_time=synthdef_builder['lag'],
                )
            amplitude = (
                synthdef_builder['gain'].db_to_amplitude() *
                (synthdef_builder['gain'] > -96.0)
                ).lag(synthdef_builder['lag'])
            total_gain = gate * active * amplitude
            source *= total_gain
            ugentools.Out.ar(
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
