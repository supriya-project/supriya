import supriya

from .. import project_settings, synthdefs


class SessionFactory(supriya.nonrealtime.SessionFactory):

    ### CLASS VARIABLES ###

    release_time = 15

    ### SESSION ###

    def __session__(self, initial_seed=0, layer_count=10, minutes=2, **kwargs):
        self.buffers = []
        session = supriya.Session(
            input_bus_channel_count=self.input_bus_channel_count,
            output_bus_channel_count=self.output_bus_channel_count,
        )
        with session.at(0):
            for say in self.libretto:
                buffer_ = session.add_buffer(channel_count=1, file_path=say)
                self.buffers.append(buffer_)
            for i in range(layer_count):
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

    @property
    def libretto(self):
        libretto = []
        text = "videoconferencing"
        for voice in ["Daniel", "Tessa", "Karen", "Thomas"]:
            libretto.append(supriya.Say(text, voice=voice))
        return libretto

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
        source_pattern = self.one_shot_player_pattern
        source_pattern = source_pattern.with_group(release_time=self.release_time)
        source_pattern = source_pattern.with_effect(
            synthdef=synthdefs.compressor_synthdef,
            release_time=self.release_time,
            pregain=3,
        )
        return source_pattern

    @property
    def one_shot_player_pattern(self):
        return supriya.patterns.Pbind(
            synthdef=synthdefs.one_shot_player_synthdef,
            add_action=supriya.AddAction.ADD_TO_HEAD,
            buffer_id=supriya.patterns.Prand(self.buffers, repetitions=None),
            delta=5,
            duration=0,
            gain=supriya.patterns.Pwhite(-12, 12),
            pan=supriya.patterns.Pwhite(-1, 1.0),
            rate=2 ** supriya.patterns.Pwhite(-1, 0.25),
        )

    ### EFFECT PATTERNS ###

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
                self.chorus_pattern,
                self.freeverb_pattern,
                self.chorus_pattern,
                self.pitchshift_pattern,
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
            level=supriya.patterns.Pwhite(0.0, 0.25),
            room_size=supriya.patterns.Pwhite() ** 0.25,
        )

    @property
    def fx_pattern(self):
        return supriya.patterns.Pbind(
            add_action=supriya.AddAction.ADD_TO_TAIL,
            delta=supriya.patterns.Pwhite(0, 10),
            duration=supriya.patterns.Pwhite(5, 30),
            level=supriya.patterns.Pwhite(0.25, 1.0),
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


chants = SessionFactory.from_project_settings(project_settings)
