import urwid


class ApplicationTUI:

    ### INITIALIZER ###

    def __init__(self, application):
        import supriya
        self._refresh_rate = 0.1
        self._application = application
        self._server_tui = supriya.livetools.ServerTUI(
            self.application.server,
            )
        self._mixer_tui = supriya.livetools.MixerTUI(
            self.application.mixer,
            )
        self._top_widget = urwid.Padding(
            urwid.Frame(
                urwid.Frame(
                    body=self.mixer_tui.widget,
                    header=self.server_tui.header_box,
                    footer=self.server_tui.footer_box,
                    ),
                header=urwid.Divider(),
                footer=urwid.Divider(),
                ),
            left=1,
            right=1,
            )
        self._loop = urwid.MainLoop(
            self._top_widget,
            palette=self.palette,
            event_loop=urwid.AsyncioEventLoop(),
            unhandled_input=self.exit_on_q,
            )

    ### PRIVATE METHODS ###

    def _refresh_loop(self, loop, *args):
        self.refresh()
        loop.set_alarm_in(self._refresh_rate, self._refresh_loop)

    ### PUBLIC METHODS ###

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def refresh(self):
        self.mixer_tui.refresh()
        self.server_tui.refresh()

    def run(self):
        self.loop.set_alarm_in(self._refresh_rate, self._refresh_loop)
        self.loop.run()

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
    def top_widget(self):
        return self._top_widget
