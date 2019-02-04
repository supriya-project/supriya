import supriya

from .. import project_settings, synthdefs
from ..materials import libretto_x


class SessionFactory(supriya.nonrealtime.SessionFactory):

    ### GLOBALS ###

    release_time = 15

    ### SESSION ###

    def __session__(self, initial_seed=0, layer_count=3, minutes=3, **kwargs):
        self.buffers = []
        session = supriya.Session(
            input_bus_channel_count=self.input_bus_channel_count,
            output_bus_channel_count=self.output_bus_channel_count,
        )
        with session.at(0):
            for say in libretto_x:
                buffer_ = session.add_buffer(channel_count=1, file_path=say)
                self.buffers.append(buffer_)
        for i in range(layer_count):
            with session.at(i * 10):
                session.inscribe(
                    self.global_pattern, duration=60 * minutes, seed=initial_seed + i
                )
        with session.at(0):
            session.add_synth(
                synthdef=synthdefs.compressor_synthdef,
                add_action="ADD_TO_TAIL",
                duration=session.duration + self.release_time,
                pregain=0,
            )
            session.set_rand_seed(initial_seed)
        return session

    ### GLOBAL PATTERN ###

    @property
    def global_pattern(self):
        global_pattern = supriya.patterns.Pgpar(
            [self.source_pattern, self.effect_pattern], release_time=self.release_time
        )
        global_pattern = global_pattern.with_bus(release_time=self.release_time)
        return global_pattern

    ### SOURCE PATTERNS ###

    @property
    def source_pattern(self):
        source_pattern = self.warp_buffer_player_pattern
        source_pattern = source_pattern.with_group(release_time=self.release_time)
        source_pattern = source_pattern.with_effect(
            synthdef=synthdefs.compressor_synthdef,
            release_time=self.release_time,
            pregain=12,
        )
        return source_pattern

    @property
    def warp_buffer_player_pattern(self):
        return supriya.patterns.Pbind(
            synthdef=supriya.patterns.Prand(
                [
                    synthdefs.warp_buffer_player_factory.build(
                        name="warp2", iterations=2
                    ),
                    synthdefs.warp_buffer_player_factory.build(
                        name="warp4", iterations=4
                    ),
                    synthdefs.warp_buffer_player_factory.build(
                        name="warp8", iterations=8
                    ),
                ],
                repetitions=None,
            ),
            add_action=supriya.AddAction.ADD_TO_HEAD,
            buffer_id=supriya.patterns.Prand(self.buffers, repetitions=None),
            delta=supriya.patterns.Pwhite(0, 30),
            duration=0,
            direction=supriya.patterns.Prand([-1, 1], repetitions=None),
            gain=supriya.patterns.Pwhite(-12, 0),
            overlaps=supriya.patterns.Prand([16, 32] * 100, None),
            # overlaps=supriya.patterns.Prand(
            #    [1, 2, 4, 8, 8, 16, 16, 16, 32, 32, 32] * 4, None,
            #    )
            rate=supriya.patterns.Pwhite(4, 128),
            # rate=supriya.patterns.Pwhite(0.5, 4),
            transpose=supriya.patterns.Pwhite(-12.0, 12.0),
        )

    ### EFFECT PATTERNS ###

    @property
    def allpass_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern, synthdef=synthdefs.windowed_allpass_synthdef, gain=0
        )

    @property
    def bpf_sweep_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_bpf_sweep_synthdef,
            delta=supriya.patterns.Pwhite(30, 90),
            duration=supriya.patterns.Pwhite(30, 60),
            gain=3,
            level=supriya.patterns.Pwhite(0.0, 0.5),
            start_frequency=supriya.patterns.Pwhite(10000, 20000),
            stop_frequency=supriya.patterns.Pwhite(100, 5000),
        )

    @property
    def chorus_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_chorus_factory.build(
                name="chorus8", iterations=8
            ),
            frequency=supriya.patterns.Pwhite() * 2,
            gain=3,
        )

    @property
    def effect_pattern(self):
        effect_pattern = supriya.patterns.Ppar(
            [
                self.allpass_pattern,
                self.chorus_pattern,
                self.freeverb_pattern,
                self.freqshift_pattern,
                self.pitchshift_pattern,
                self.bpf_sweep_pattern,
                self.lpf_dip_pattern,
            ]
        )
        effect_pattern = effect_pattern.with_group(release_time=self.release_time)
        effect_pattern = effect_pattern.with_effect(
            synthdef=synthdefs.compressor_synthdef,
            release_time=self.release_time,
            pregain=3,
        )
        return effect_pattern

    @property
    def freeverb_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_freeverb_synthdef,
            damping=supriya.patterns.Pwhite() ** 0.25,
            gain=3,
            room_size=supriya.patterns.Pwhite() ** 0.25,
        )

    @property
    def freqshift_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            level=supriya.patterns.Pwhite(0.5, 1.0),
            synthdef=synthdefs.windowed_freqshift_synthdef,
            sign=supriya.patterns.Prand([-1, 1]),
        )

    @property
    def fx_pattern(self):
        return supriya.patterns.Pbind(
            add_action=supriya.AddAction.ADD_TO_TAIL,
            delta=supriya.patterns.Pwhite(15, 60),
            duration=supriya.patterns.Pwhite(30, 90),
            level=supriya.patterns.Pwhite(0.25, 1.0),
        )

    @property
    def lpf_dip_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_lpf_dip_synthdef,
            delta=supriya.patterns.Pwhite(30, 90),
            duration=supriya.patterns.Pwhite(30, 60),
            gain=3,
            level=supriya.patterns.Pwhite(0.0, 0.5),
            frequency=supriya.patterns.Pwhite(1000, 10000),
        )

    @property
    def pitchshift_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_pitchshift_synthdef,
            gain=3,
            pitch_dispersion=supriya.patterns.Pwhite(0.0, 0.02),
            pitch_shift=supriya.patterns.Pwhite(-12.0, 12.0),
            time_dispersion=supriya.patterns.Pwhite(),
            window_size=supriya.patterns.Pwhite(0.1, 2.0),
        )


choral_wash = SessionFactory.from_project_settings(project_settings)
