import supriya

from .. import project_settings, synthdefs
from ..materials import libretto_x


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
        source_pattern = self.one_shot_player_pattern
        source_pattern = source_pattern.with_group(release_time=self.release_time)
        source_pattern = source_pattern.with_effect(
            synthdef=synthdefs.compressor_synthdef,
            release_time=self.release_time,
            pregain=12,
        )
        return source_pattern

    @property
    def one_shot_player_pattern(self):
        return supriya.patterns.Pbind(
            synthdef=synthdefs.one_shot_player_synthdef,
            add_action=supriya.AddAction.ADD_TO_HEAD,
            buffer_id=supriya.patterns.Prand(self.buffers, repetitions=None),
            delta=supriya.patterns.Pwhite(0, 10),
            duration=0,
            gain=supriya.patterns.Pwhite(-12, 12),
            pan=supriya.patterns.Pwhite(-1, 1.0),
            rate=2 ** supriya.patterns.Pwhite(-1.5, 0.5),
        )

    ### EFFECT PATTERNS ###

    @property
    def allpass_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern, synthdef=synthdefs.windowed_allpass_synthdef, gain=0
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
                self.allpass_pattern,
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
            level=supriya.patterns.Pwhite(0.125, 0.5),
            room_size=supriya.patterns.Pwhite() ** 0.25,
        )

    @property
    def freqshift_pattern(self):
        return supriya.patterns.Pbindf(
            self.fx_pattern,
            level=2 ** supriya.patterns.Pwhite(-4, -2),
            synthdef=synthdefs.windowed_freqshift_synthdef,
            sign=supriya.patterns.Prand([-1, 1]),
        )

    @property
    def fx_pattern(self):
        return supriya.patterns.Pbind(
            add_action=supriya.AddAction.ADD_TO_TAIL,
            delta=supriya.patterns.Pwhite(0, 10),
            duration=supriya.patterns.Pwhite(5, 30),
            level=supriya.patterns.Pwhite(0.25, 1.0),
        )


lost_and_found = SessionFactory.from_project_settings(project_settings)
