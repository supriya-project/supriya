import urwid


class TrackDetailTUI:

    def __init__(self, track):
        self._track = track
        widget = urwid.Columns([
            self._attr_mapped(urwid.LineBox(urwid.Filler(urwid.Text('A')))),
            self._attr_mapped(urwid.LineBox(urwid.Filler(urwid.Text('B')))),
            self._attr_mapped(urwid.LineBox(urwid.Filler(urwid.Text('C')))),
            urwid.Filler(urwid.Text('')),
            ])
        widget = urwid.AttrMap(widget, 'blur', focus_map={None: 'focus'})
        self._widget = widget

    def _attr_mapped(self, widget):
        return urwid.AttrMap(
            widget,
            None,
            focus_map={None: 'local-focus'},
            )

    @property
    def track(self):
        return self._track

    @property
    def widget(self):
        return self._widget
