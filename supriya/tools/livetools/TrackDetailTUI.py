import urwid
from supriya.tools.livetools.LeftLineBox import LeftLineBox


class TrackDetailTUI:

    def __init__(self, track, application_tui=None):
        self._application_tui = application_tui
        self._track = track
        columns = []
        columns.append(self._build_direct_ins_widget())
        for slot in self.track._slots:
            columns.append(self._build_slot_widget(slot))
        columns.append(urwid.Filler(urwid.Text('')))
        columns.append(self._build_sends_widget())
        columns.append(self._build_direct_outs_widget())
        widget = urwid.Columns(columns)
        widget = urwid.AttrMap(widget, 'blur', focus_map={None: 'focus'})
        self._widget = widget

    def _attr_mapped(self, widget):
        return urwid.AttrMap(
            widget,
            None,
            focus_map={None: 'local-focus'},
            )

    def _build_slot_widget(self, slot):
        return LeftLineBox(
            urwid.Filler(
                urwid.Text('Slot: {}'.format(slot.name)),
                valign='top',
                ),
            title='Slot "{}"'.format(slot.name),
            )

    def _build_sends_widget(self):
        pile = [urwid.Text('Sends')]
        for send in self.track._outgoing_sends:
            pile.append(urwid.Text('Send: {}'.format(send)))
        return LeftLineBox(
            urwid.Filler(
                urwid.Pile(pile),
                valign='top',
                ),
            title='Sends',
            )

    def _build_direct_ins_widget(self):
        checkbox_rows = []
        server = self.track.mixer.server
        if server is not None:
            output_count = server.server_options.input_bus_channel_count
        else:
            output_count = 8
        for _ in range(output_count):
            cells = []
            for _ in range(self.track.channel_count):
                cells.append(urwid.CheckBox(''))
            checkbox_row = urwid.GridFlow(cells, 4, 0, 0, 'left')
            checkbox_rows.append(checkbox_row)
        pile = urwid.Pile(checkbox_rows)
        return LeftLineBox(
            urwid.Padding(
                urwid.Filler(pile, valign='top', top=1, bottom=1),
                left=1,
                right=1,
                ),
            title='D.I.',
            )

    def _build_direct_outs_widget(self):
        checkbox_rows = []
        server = self.track.mixer.server
        if server is not None:
            output_count = server.server_options.output_bus_channel_count
        else:
            output_count = 8
        for _ in range(output_count):
            cells = []
            for _ in range(self.track.channel_count):
                cells.append(urwid.CheckBox(''))
            checkbox_row = urwid.GridFlow(cells, 4, 0, 0, 'left')
            checkbox_rows.append(checkbox_row)
        pile = urwid.Pile(checkbox_rows)
        return LeftLineBox(urwid.Filler(pile, valign='top'), title='D.O.')

    @property
    def track(self):
        return self._track

    @property
    def widget(self):
        return self._widget
