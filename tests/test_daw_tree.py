from uqbar.strings import normalize

from supriya.daw import (
    Application,
    AudioDevice,
    AudioRack,
    GroupTrack,
    Instrument,
    InstrumentRack,
    MidiDevice,
)


def test_01():
    app = Application()
    track_a = app.add_track()
    track_b = app.add_track()
    track_c = app.add_track()
    GroupTrack.group([track_a, track_b])
    instrument_rack = InstrumentRack()
    instrument_rack.add_chain().devices.extend(
        [MidiDevice(), Instrument(), AudioDevice()]
    )
    audio_rack = AudioRack()
    audio_rack.add_chain().devices.append(AudioDevice())
    track_b.devices.append(instrument_rack)
    track_c.devices.append(audio_rack)
    print("Booting...")
    app.boot()
    assert str(app.node) == normalize(
        """
        1000 group (application)
            1001 transport (transport)
                beats_per_minute: 120.0, denominator: 4.0, numerator: 4.0
            1002 group (track container)
                1003 group (group track)
                    1004 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 24.0, lag: 0.1, out: 26.0
                    1005 group (track container)
                        1006 group (track)
                            1007 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 28.0, lag: 0.1, out: 30.0
                            1008 group (device container)
                            1009 group (pre-fader sends)
                            1010 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 30.0
                            1011 group (post-fader sends)
                                1012 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 30.0, lag: 0.1, out: 26.0
                        1013 group (track)
                            1014 mixer/track-input/2
                                active: 1.0, gain: 0.0, gate: 1.0, in_: 32.0, lag: 0.1, out: 34.0
                            1015 group (device container)
                                1016 group (instrument rack)
                                    1017 group (chain container)
                                        1018 group (instrument chain)
                                            1019 group (device container)
                                                1020 group (instrument)
                                                1021 group (audio device)
                                            1022 group (pre-fader sends)
                                            1023 mixer/chain-output/2
                                                active: 1.0, gain: 0.0, gate: 1.0, in_: 38.0, lag: 0.1, out: 38.0
                                            1024 group (post-fader sends)
                                                1025 mixer/send/2x2 (to instrument rack)
                                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 38.0, lag: 0.1, out: 36.0
                                    1026 group (return chain container)
                                    1027 mixer/rack-output/2 (rack output)
                                        active: 1.0, gate: 1.0, in_: 36.0, lag: 0.1, out: 34.0
                            1028 group (pre-fader sends)
                            1029 mixer/track-output/2
                                active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 34.0
                            1030 group (post-fader sends)
                                1031 mixer/send/2x2 (to group track)
                                    active: 1.0, gain: 0.0, gate: 1.0, in_: 34.0, lag: 0.1, out: 26.0
                    1032 group (device container)
                    1033 group (pre-fader sends)
                    1034 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 26.0
                    1035 group (post-fader sends)
                        1066 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 26.0, lag: 0.1, out: 22.0
                1036 group (track)
                    1037 mixer/track-input/2
                        active: 1.0, gain: 0.0, gate: 1.0, in_: 40.0, lag: 0.1, out: 42.0
                    1038 group (device container)
                        1039 group (audio rack)
                            1040 group (chain container)
                                1041 group (audio chain)
                                    1042 mixer/chain-input/2
                                        active: 1.0, gate: 1.0, in_: 42.0, lag: 0.1, out: 46.0
                                    1043 group (device container)
                                        1044 group (audio device)
                                    1045 group (pre-fader sends)
                                    1046 mixer/chain-output/2
                                        active: 1.0, gain: 0.0, gate: 1.0, in_: 46.0, lag: 0.1, out: 46.0
                                    1047 group (post-fader sends)
                                        1048 mixer/send/2x2 (to audio rack)
                                            active: 1.0, gain: 0.0, gate: 1.0, in_: 46.0, lag: 0.1, out: 44.0
                            1049 mixer/rack-output/2 (rack output)
                                active: 1.0, gate: 1.0, in_: 44.0, lag: 0.1, out: 42.0
                    1050 group (pre-fader sends)
                    1051 mixer/track-output/2
                        active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 42.0
                    1052 group (post-fader sends)
                        1067 mixer/send/2x2 (to master track)
                            active: 1.0, gain: 0.0, gate: 1.0, in_: 42.0, lag: 0.1, out: 22.0
            1053 group (return track container)
            1054 group (master track)
                1055 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 20.0, lag: 0.1, out: 22.0
                1056 group (device container)
                1057 group (pre-fader sends)
                1058 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 22.0
                1059 group (post-fader sends)
            1060 group (cue track)
                1061 mixer/track-input/2
                    active: 1.0, gain: 0.0, gate: 1.0, in_: 16.0, lag: 0.1, out: 18.0
                1062 group (device container)
                1063 group (pre-fader sends)
                1064 mixer/track-output/2
                    active: 1.0, gain: 0.0, gate: 1.0, lag: 0.1, out: 18.0
                1065 group (post-fader sends)
        """
    )
