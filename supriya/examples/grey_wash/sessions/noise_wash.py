import supriya

from .. import project_settings, synthdefs


class SessionFactory(supriya.nonrealtime.SessionFactory):

    ### GLOBALS ###

    release_time = 15

    ### SESSION ###

    def __session__(self, initial_seed=0, layer_count=10, minutes=3):
        session = supriya.Session(
            input_bus_channel_count=self.input_bus_channel_count,
            output_bus_channel_count=self.output_bus_channel_count,
        )
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
        source_pattern = supriya.patterns.Ppar([self.noise_wash_pattern])
        source_pattern = source_pattern.with_group(release_time=self.release_time)
        source_pattern = source_pattern.with_effect(
            synthdef=synthdefs.compressor_synthdef,
            release_time=self.release_time,
            pregain=12,
        )
        return source_pattern

    @property
    def noise_wash_pattern(self):
        return supriya.patterns.Pbind(
            synthdef=synthdefs.noise_wash_synthdef,
            delta=supriya.patterns.Pwhite(15, 30),
            duration=supriya.patterns.Pwhite(15, 60),
            gain=supriya.patterns.Pwhite(-12, 0),
        )

    ### EFFECT PATTERNS ###

    @property
    def effect_pattern(self):
        effect_pattern = supriya.patterns.Pgpar(
            [
                [
                    self.allpass_pattern,
                    self.chorus_pattern,
                    self.freeverb_pattern,
                    self.freqshift_pattern,
                    self.pitchshift_pattern,
                    self.lpf_dip_pattern,
                    self.bpf_sweep_pattern,
                    self.lp_flicker_pattern,
                ]
            ],
            release_time=self.release_time,
        )
        effect_pattern = effect_pattern.with_group(release_time=self.release_time)
        effect_pattern = effect_pattern.with_effect(
            synthdef=synthdefs.compressor_synthdef,
            release_time=self.release_time,
            pregain=3,
        )
        return effect_pattern

    @property
    def fx_pattern(self):
        return supriya.patterns.Pbind(
            add_action=supriya.AddAction.ADD_TO_TAIL,
            delta=supriya.patterns.Pwhite(15, 30),
            duration=supriya.patterns.Pwhite(30, 90),
            gain=0,
            level=supriya.patterns.Pwhite(0.25, 0.75),
        )

    @property
    def bpf_sweep_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_bpf_sweep_synthdef,
            delta=supriya.patterns.Pwhite(30, 90),
            duration=supriya.patterns.Pwhite(30, 60),
            gain=0,
            level=supriya.patterns.Pwhite(0.0, 0.5),
            start_frequency=supriya.patterns.Pwhite(10000, 20000),
            stop_frequency=supriya.patterns.Pwhite(100, 5000),
        )

    @property
    def lpf_dip_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_lpf_dip_synthdef,
            delta=supriya.patterns.Pwhite(30, 90),
            duration=supriya.patterns.Pwhite(30, 60),
            gain=1,
            level=supriya.patterns.Pwhite(0.0, 0.5),
            frequency=supriya.patterns.Pwhite(1000, 10000),
        )

    @property
    def pitchshift_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            gain=1,
            pitch_dispersion=supriya.patterns.Pwhite(0.0, 0.02),
            pitch_shift=supriya.patterns.Pwhite(-12.0, 12.0),
            synthdef=synthdefs.windowed_pitchshift_synthdef,
            time_dispersion=supriya.patterns.Pwhite(),
            window_size=supriya.patterns.Pwhite(0.1, 2.0),
            level=supriya.patterns.Pwhite(0.75, 1.0),
        )

    @property
    def allpass_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            gain=0,
            synthdef=synthdefs.windowed_allpass_synthdef,
            level=supriya.patterns.Pwhite(0.75, 1.0),
        )

    @property
    def chorus_pattern(self):
        choruses = [
            synthdefs.windowed_chorus_factory.build(name="chorus2", iterations=2),
            synthdefs.windowed_chorus_factory.build(name="chorus4", iterations=4),
            synthdefs.windowed_chorus_factory.build(name="chorus8", iterations=8),
        ]
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            gain=1,
            synthdef=supriya.patterns.Pseq(choruses, None),
            level=supriya.patterns.Pwhite(0.5, 1.0),
        )

    @property
    def freeverb_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            synthdef=synthdefs.windowed_freeverb_synthdef,
            damping=supriya.patterns.Pwhite(0.5, 1),
            gain=0,
            room_size=supriya.patterns.Pwhite(0.5, 1),
        )

    @property
    def freqshift_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            gain=1,
            level=supriya.patterns.Pwhite(0.75, 1.0),
            sign=supriya.patterns.Prand([-1, 1]),
            synthdef=synthdefs.windowed_freqshift_synthdef,
        )

    @property
    def lp_flicker_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            duration=supriya.patterns.Pwhite(15, 30),
            synthdef=synthdefs.lp_flicker_synthdef,
            level=1.0,
        )


noise_wash = SessionFactory.from_project_settings(project_settings)
