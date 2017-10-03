import urwid
from supriya.tools.livetools.TrackDetailTUI import TrackDetailTUI


class ApplicationTUI:

    ### INITIALIZER ###

    def __init__(self, application):
        import supriya
        self._refresh_rate = 0.1
        self._application = application
        self._server_tui = supriya.livetools.ServerTUI(
            self.application.server,
            application_tui=self,
            )
        self._mixer_tui = supriya.livetools.MixerTUI(
            self.application.mixer,
            application_tui=self,
            )

        self._mixer_widget = self._mixer_tui.widget
        self._track_details_widget = urwid.WidgetPlaceholder(
            urwid.LineBox(
                urwid.Filler(
                    urwid.Text('details', align='center'),
                    ),
                ),
            )

        self._foreground_widget = urwid.Padding(
            urwid.Frame(
                urwid.Frame(
                    body=urwid.Pile([
                        ('weight', 2, self._mixer_widget),
                        (1, urwid.SolidFill('-')),
                        ('weight', 1, self._track_details_widget),
                        ]),
                    header=self.server_tui.header_box,
                    footer=self.server_tui.footer_box,
                    ),
                header=urwid.Divider(),
                footer=urwid.Divider(),
                ),
            left=1,
            right=1,
            )
        self._background_widget = self._foreground_widget
        self._loop = urwid.MainLoop(
            self._foreground_widget,
            palette=self.palette,
            event_loop=urwid.AsyncioEventLoop(),
            unhandled_input=self.unhandled_input,
            )

    ### PRIVATE METHODS ###

    def _attr_mapped(self, widget):
        return urwid.AttrMap(
            widget,
            None,
            focus_map={None: 'local-focus'},
            )

    def _refresh_loop(self, loop, *args):
        self.refresh()
        loop.set_alarm_in(self._refresh_rate, self._refresh_loop)

    ### PUBLIC METHODS ###

    def add_overlay(self, widget):
        self._foreground_widget = widget
        self._loop.widget = urwid.Overlay(
            self.foreground_widget,
            self.background_widget,
            ('fixed left', 10),
            ('fixed right', 10),
            ('fixed top', 10),
            ('fixed bottom', 10),
            )

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key == 'esc':
            self.remove_overlay()
        elif key in ('12345678'):
            index = int(key) - 1
            if index >= len(self._mixer_tui._track_tuis):
                return
            self._mixer_tui._widget.set_focus_path([index])
        elif key == '9':
            contents_length = len(self._mixer_tui._widget.contents)
            self._mixer_tui._widget.set_focus_path([contents_length - 2])
        elif key == '0':
            contents_length = len(self._mixer_tui._widget.contents)
            self._mixer_tui._widget.set_focus_path([contents_length - 1])

    def update_track_details(self, track):
        track_detail_tui = TrackDetailTUI(track, application_tui=self)
        widget = track_detail_tui.widget
        self._track_details_widget.original_widget = widget

    def refresh(self):
        self.mixer_tui.refresh()
        self.server_tui.refresh()

    def run(self):
        track = self.application.mixer.master_track
        if self.application.mixer.tracks:
            track = self.application.mixer.tracks[0]
        self.update_track_details(track)
        self.loop.set_alarm_in(self._refresh_rate, self._refresh_loop)
        self.loop.run()

    def remove_overlay(self):
        if self.foreground_widget is self.background_widget:
            return
        self._foreground_widget = self._background_widget
        self._loop.widget = self._foreground_widget

    ### PUBLIC PROPERTIES ###

    @property
    def application(self):
        return self._application

    @property
    def loop(self):
        return self._loop

    @property
    def mixer_tui(self):
        return self._mixer_tui

    @property
    def palette(self):
        return [
            ('default', '', ''),
            ('bargraph-background', 'bold', ''),
            ('bargraph-1', 'dark cyan', '', ''),
            ('bargraph-1-smooth', 'dark cyan', ''),
            ('bargraph-2', '', 'brown', ''),
            ('bargraph-2-smooth', 'brown', ''),
            ('blur', 'dark gray', ''),
            ('focus', 'white', ''),
            ('local-focus', 'white,bold', 'dark cyan'),
            ]

    @property
    def server_tui(self):
        return self._server_tui

    @property
    def background_widget(self):
        return self._background_widget

    @property
    def foreground_widget(self):
        return self._foreground_widget
