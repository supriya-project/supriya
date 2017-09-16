import urwid


class MixerTUI:

    ### INITIALIZER ###

    def __init__(self, mixer):
        import supriya
        self._mixer = mixer
        self._cue_track_tui = supriya.livetools.TrackTUI(
            self._mixer.cue_track,
            )
        self._master_track_tui = supriya.livetools.TrackTUI(
            self._mixer.master_track,
            )
        self._track_tuis = [
            supriya.livetools.TrackTUI(track)
            for track in self._mixer.tracks
            ]
        self._widget = urwid.Columns([
            (20, track_tui.widget)
            for track_tui in self._track_tuis
            ] + [
            urwid.Filler(urwid.Text('')),
            (
                42,
                urwid.LineBox(
                    urwid.Columns([
                        (20, self._cue_track_tui.widget),
                        (20, self._master_track_tui.widget),
                        ]),
                    ),
            ),
            ],
            dividechars=1,
            )

    ### PUBLIC METHODS ###

    def refresh(self):
        for track_tui in self.track_tuis:
            track_tui.refresh()
        self.cue_track_tui.refresh()
        self.master_track_tui.refresh()

    ### PUBLIC PROPERTIES ###

    @property
    def cue_track_tui(self):
        return self._cue_track_tui

    @property
    def master_track_tui(self):
        return self._master_track_tui

    @property
    def mixer(self):
        return self._mixer

    @property
    def track_tuis(self):
        return self._track_tuis

    @property
    def widget(self):
        return self._widget
