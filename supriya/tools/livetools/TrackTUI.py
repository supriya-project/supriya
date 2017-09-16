import math
import random
import urwid
from supriya.tools.livetools.BoundCheckBox import BoundCheckBox
from supriya.tools.livetools.BoundGainButton import BoundGainButton


class TrackTUI:

    ### INITIALIZER ###

    def __init__(self, track):
        self._track = track
        # Buttons
        self._direct_ins_button = urwid.Button('Direct Ins')
        self._direct_outs_button = urwid.Button('Direct Outs')
        self._sends_button = urwid.Button('Sends')
        self._slots_button = urwid.Button('Slots')
        # CheckBoxes
        if self.track.name != 'cue':
            cue_checkbox = None
        else:
            cue_checkbox = BoundCheckBox(
                'Cue',
                self.track.get_cue,
                self.track.set_cue,
                )
        if self.track.name in ('cue', 'master'):
            mute_checkbox = None
            solo_checkbox = None
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
            if checkbox is not None
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
        # Widgets
        header = urwid.BoxAdapter(
            urwid.ListBox(
                urwid.SimpleListWalker([
                    self._attr_mapped(self._direct_ins_button),
                    urwid.LineBox(
                        urwid.BoxAdapter(
                            self._input_graph,
                            height=4,
                            ),
                        title='Inputs',
                        ),
                    ]),
                ),
            height=7,
            )
        footer = urwid.BoxAdapter(
            urwid.ListBox(
                urwid.SimpleListWalker([
                    urwid.LineBox(
                        urwid.BoxAdapter(
                            urwid.AttrMap(
                                self._prefader_graph,
                                'bargraph-1',
                                focus_map={None: 'focus'},
                                ),
                            height=4,
                            ),
                        title='Prefader',
                        ),
                    *self._checkboxes,
                    self._attr_mapped(self._gain_slider),
                    urwid.LineBox(
                        urwid.BoxAdapter(
                            self._postfader_graph,
                            height=4,
                            ),
                        title='Postfader',
                        ),
                    self._attr_mapped(self._direct_outs_button),
                    ]),
                ),
            height=17,
            )
        body = urwid.ListBox(
            urwid.SimpleListWalker([
                self._slots_button,
                self._sends_button,
                ]),
            )
        self._widget = urwid.LineBox(
            urwid.Pile([('pack', header), body, ('pack', footer)]),
            title=self.track.name,
            )
        self._widget = urwid.AttrMap(self._widget, 'blur', focus_map={None: 'focus'})

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
            checkbox.original_widget.refresh()
        # Sliders
        self._gain_slider.refresh()

    ### PUBLIC PROPERTIES ###

    @property
    def track(self):
        return self._track

    @property
    def widget(self):
        return self._widget
