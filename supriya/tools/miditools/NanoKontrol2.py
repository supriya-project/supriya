# -*- encoding: utf-8- -*-
from supriya.tools.miditools.MidiDevice import MidiDevice


class NanoKontrol2(MidiDevice):
    r'''A Korg NanoKontrol2 midi device.

    ::

        >>> nano_kontrol_2 = miditools.NanoKontrol2()
        >>> nano_kontrol_2
        NanoKontrol2()

    ::

        >>> len(nano_kontrol_2)
        51

    ::

        >>> for control_name in nano_kontrol_2:
        ...     control_name
        ...
        'fader_1'
        'fader_2'
        'fader_3'
        'fader_4'
        'fader_5'
        'fader_6'
        'fader_7'
        'fader_8'
        'knob_1'
        'knob_2'
        'knob_3'
        'knob_4'
        'knob_5'
        'knob_6'
        'knob_7'
        'knob_8'
        'm_button_1'
        'm_button_2'
        'm_button_3'
        'm_button_4'
        'm_button_5'
        'm_button_6'
        'm_button_7'
        'm_button_8'
        'r_button_1'
        'r_button_2'
        'r_button_3'
        'r_button_4'
        'r_button_5'
        'r_button_6'
        'r_button_7'
        'r_button_8'
        's_button_1'
        's_button_2'
        's_button_3'
        's_button_4'
        's_button_5'
        's_button_6'
        's_button_7'
        's_button_8'
        'transport_cycle_button'
        'transport_fastforward_button'
        'transport_next_marker_button'
        'transport_next_track_button'
        'transport_play_button'
        'transport_previous_marker_button'
        'transport_previous_track_button'
        'transport_record_button'
        'transport_rewind_button'
        'transport_set_marker_button'
        'transport_stop_button'

    ::

        >>> nano_kontrol_2.fader_1
        MidiFader(
            controller_number=0
            )

    ::

        >>> nano_kontrol_2['fader_1']
        MidiFader(
            controller_number=0
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        from supriya.tools import miditools
        midi_controls = {
            'fader_1': miditools.MidiFader(controller_number=0),
            'fader_2': miditools.MidiFader(controller_number=1),
            'fader_3': miditools.MidiFader(controller_number=2),
            'fader_4': miditools.MidiFader(controller_number=3),
            'fader_5': miditools.MidiFader(controller_number=4),
            'fader_6': miditools.MidiFader(controller_number=5),
            'fader_7': miditools.MidiFader(controller_number=6),
            'fader_8': miditools.MidiFader(controller_number=7),
            'knob_1': miditools.MidiFader(controller_number=16),
            'knob_2': miditools.MidiFader(controller_number=17),
            'knob_3': miditools.MidiFader(controller_number=18),
            'knob_4': miditools.MidiFader(controller_number=19),
            'knob_5': miditools.MidiFader(controller_number=20),
            'knob_6': miditools.MidiFader(controller_number=21),
            'knob_7': miditools.MidiFader(controller_number=22),
            'knob_8': miditools.MidiFader(controller_number=23),
            'm_button_1': miditools.MidiButton(controller_number=48),
            'm_button_2': miditools.MidiButton(controller_number=49),
            'm_button_3': miditools.MidiButton(controller_number=50),
            'm_button_4': miditools.MidiButton(controller_number=51),
            'm_button_5': miditools.MidiButton(controller_number=52),
            'm_button_6': miditools.MidiButton(controller_number=53),
            'm_button_7': miditools.MidiButton(controller_number=54),
            'm_button_8': miditools.MidiButton(controller_number=55),
            'r_button_1': miditools.MidiButton(controller_number=64),
            'r_button_2': miditools.MidiButton(controller_number=65),
            'r_button_3': miditools.MidiButton(controller_number=66),
            'r_button_4': miditools.MidiButton(controller_number=67),
            'r_button_5': miditools.MidiButton(controller_number=68),
            'r_button_6': miditools.MidiButton(controller_number=69),
            'r_button_7': miditools.MidiButton(controller_number=70),
            'r_button_8': miditools.MidiButton(controller_number=71),
            's_button_1': miditools.MidiButton(controller_number=32),
            's_button_2': miditools.MidiButton(controller_number=33),
            's_button_3': miditools.MidiButton(controller_number=34),
            's_button_4': miditools.MidiButton(controller_number=35),
            's_button_5': miditools.MidiButton(controller_number=36),
            's_button_6': miditools.MidiButton(controller_number=37),
            's_button_7': miditools.MidiButton(controller_number=38),
            's_button_8': miditools.MidiButton(controller_number=39),
            'transport_cycle_button': miditools.MidiButton(controller_number=46),
            'transport_fastforward_button': miditools.MidiButton(controller_number=44),
            'transport_next_marker_button': miditools.MidiButton(controller_number=62),
            'transport_next_track_button': miditools.MidiButton(controller_number=59),
            'transport_play_button': miditools.MidiButton(controller_number=41),
            'transport_previous_marker_button': miditools.MidiButton(controller_number=61),
            'transport_previous_track_button': miditools.MidiButton(controller_number=58),
            'transport_record_button': miditools.MidiButton(controller_number=45),
            'transport_rewind_button': miditools.MidiButton(controller_number=43),
            'transport_set_marker_button': miditools.MidiButton(controller_number=60),
            'transport_stop_button': miditools.MidiButton(controller_number=42),
            }
        MidiDevice.__init__(
            self,
            midi_controls=midi_controls,
            )