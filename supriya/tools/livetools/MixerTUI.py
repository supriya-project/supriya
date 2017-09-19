import urwid
from supriya.tools.livetools.FocusColumns import FocusColumns


class MixerTUI:

    ### INITIALIZER ###

    def __init__(self, mixer, application_tui=None):
        import supriya
        self._mixer = mixer
        self._application_tui = application_tui
        self._cue_track_tui = supriya.livetools.TrackSummaryTUI(
            self._mixer.cue_track,
            application_tui=application_tui,
            )
        self._master_track_tui = supriya.livetools.TrackSummaryTUI(
            self._mixer.master_track,
            application_tui=application_tui,
            )
        self._track_tuis = [
            supriya.livetools.TrackSummaryTUI(
                track,
                application_tui=application_tui,
                )
            for track in self._mixer.tracks
            ]
        columns = []
        for track_tui in self._track_tuis:
            columns.append((20, track_tui.widget))
        columns.append(urwid.Filler(urwid.Text(''))),
        columns.append((20, self._cue_track_tui.widget))
        columns.append((20, self._master_track_tui.widget))
        self._widget = FocusColumns(columns, dividechars=1)
        urwid.connect_signal(
            self._widget,
            'modified',
            lambda x: self._update_track_details(),
            )

    ### PRIVATE METHODS ###

    def _update_track_details(self):
        focus_position = self._widget.focus_position
        max_position = len(self._widget.contents) - 1
        track = None
        if focus_position < len(self.mixer.tracks):
            track = self.mixer.tracks[focus_position]
        elif focus_position == max_position:
            track = self.mixer.master_track
            #raise Exception(focus_position, max_position, track)
        elif focus_position == max_position - 1:
            track = self.mixer.cue_track
            #raise Exception(focus_position, max_position, track)
        if track is not None:
            self._application_tui.update_track_details(track)

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
