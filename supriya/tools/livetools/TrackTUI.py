import math
import random
import urwid
from supriya.tools.livetools.GainButton import GainButton


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
        self._cue_checkbox = urwid.CheckBox('Cue')
        self._mute_checkbox = urwid.CheckBox('Mute')
        self._solo_checkbox = urwid.CheckBox('Solo')
        # Sliders
        self._gain_slider = GainButton('Gain')
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
                    self._attr_mapped(self._mute_checkbox),
                    self._attr_mapped(self._solo_checkbox),
                    self._attr_mapped(self._cue_checkbox),
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
        self._cue_checkbox.set_state(self.track.is_cued, do_callback=False)
        self._mute_checkbox.set_state(self.track.is_muted, do_callback=False)
        self._solo_checkbox.set_state(self.track.is_soloed, do_callback=False)

    ### PUBLIC PROPERTIES ###

    @property
    def track(self):
        return self._track

    @property
    def widget(self):
        return self._widget
