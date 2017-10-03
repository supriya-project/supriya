import math
import random
import urwid
from supriya.tools.livetools.BoundCheckBox import BoundCheckBox
from supriya.tools.livetools.BoundGainButton import BoundGainButton


class TrackSummaryTUI:

    ### INITIALIZER ###

    def __init__(self, track, application_tui=None):
        self._track = track
        self._application_tui = application_tui
        self._setup_interactive_widgets()
        self._setup_aggregate_widgets()

    ### PRIVATE METHODS ###

    def _attr_mapped(self, widget):
        return urwid.AttrMap(
            widget,
            None,
            focus_map={None: 'local-focus'},
            )

    def _get_levels(self, levels):
        if levels:
            levels = levels['rms']
        else:
            levels = [0.0]
        decibels = []
        for level in levels:
            if level > 0:
                decibels.append(20 * math.log10(level))
            else:
                decibels.append(float('-inf'))
        return decibels

    def _make_graph(self):
        import supriya
        graph = supriya.livetools.BarGraph()
        data = [random.randint(0, 100) for _ in range(8)]
        graph.set_data(data, 0, 100)
        return graph

    def _setup_aggregate_widgets(self):
        self._widget = urwid.AttrMap(
            urwid.LineBox(
                urwid.ListBox(
                    urwid.SimpleListWalker([
                        urwid.Text('{} Channels'.format(
                            self.track.channel_count),
                            align='center',
                            ),
                        urwid.LineBox(
                            urwid.BoxAdapter(
                                self._input_graph,
                                height=6,
                                ),
                            title='Inputs',
                            ),
                        self._slots_button,
                        urwid.LineBox(
                            urwid.BoxAdapter(
                                self._prefader_graph,
                                height=6,
                                ),
                            title='Prefader',
                            ),
                        *self._checkboxes,
                        self._attr_mapped(self._gain_slider),
                        urwid.LineBox(
                            urwid.BoxAdapter(
                                self._postfader_graph,
                                height=6,
                                ),
                            title='Postfader',
                            ),
                        self._sends_button,
                        ]),
                    ),
                title=self.track.name,
                ),
            'blur',
            focus_map={None: 'focus'},
            )

    def _setup_interactive_widgets(self):
        # Buttons
        self._sends_button = urwid.Button('Sends')
        self._slots_button = urwid.Button('Slots')
        # CheckBoxes
        if self.track.name == 'cue':
            cue_checkbox = urwid.Divider()
        else:
            cue_checkbox = BoundCheckBox(
                'Cue',
                self.track.get_cue,
                self.track.set_cue,
                )
        if self.track.name in ('cue', 'master'):
            mute_checkbox = urwid.Divider()
            solo_checkbox = urwid.Divider()
        else:
            mute_checkbox = BoundCheckBox(
                'Mute',
                self.track.get_mute,
                self.track.set_mute,
                )
            solo_checkbox = BoundCheckBox(
                'Solo',
                self.track.get_solo,
                self.track.set_solo,
                )
        self._checkboxes = [
            self._attr_mapped(checkbox)
            for checkbox in [cue_checkbox, mute_checkbox, solo_checkbox]
            ]
        # Sliders
        self._gain_slider = BoundGainButton(
            'Gain',
            read_source=self.track.get_gain,
            write_source=self.track.set_gain,
            )
        # Graphs
        self._input_graph = self._make_graph()
        self._postfader_graph = self._make_graph()
        self._prefader_graph = self._make_graph()

    ### PUBLIC METHODS ###

    def refresh(self):
        # input levels
        input_levels = self._get_levels(self.track.input_levels)
        self._input_graph.set_data(input_levels, -64.0, 0.0)
        # prefader levels
        prefader_levels = self._get_levels(self.track.prefader_levels)
        self._prefader_graph.set_data(prefader_levels, -64.0, 0.0)
        # postfader levels
        postfader_levels = self._get_levels(self.track.postfader_levels)
        self._postfader_graph.set_data(postfader_levels, -64.0, 0.0)
        # checkboxes
        for checkbox in self._checkboxes:
            checkbox = checkbox.original_widget
            if 'refresh' in dir(checkbox):
                checkbox.refresh()
        # Sliders
        self._gain_slider.refresh()

    ### PUBLIC PROPERTIES ###

    @property
    def track(self):
        return self._track

    @property
    def widget(self):
        return self._widget
