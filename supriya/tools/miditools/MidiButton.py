# -*- encoding: utf-8- -*-
from supriya.tools import bindingtools
from supriya.tools.miditools.MidiController import MidiController


class MidiButton(MidiController):

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        controller_number=None,
        invert=False,
        ):
        MidiController.__init__(
            self,
            channel_number=channel_number,
            controller_number=controller_number,
            )
        self._invert = bool(invert)
        self._on_press = bindingtools.BindingSource()
        self._on_release = bindingtools.BindingSource()
        self._previous_value = False

    ### SPECIAL METHODS ###

    def __call__(self, message):
        value = bool(message.controller_value)
        if self._invert:
            value = not value
        self._send_bound_event(value)
        if value != self._previous_value:
            self._on_change._send_bound_event(value)
        if not self._previous_value and value:
            self._on_press._send_bound_event(value)
        if self._previous_value and not value:
            self._on_release._send_bound_event(value)
        self._previous_value = value

    ### PUBLIC PROPERTIES ###

    @property
    def invert(self):
        return self._invert

    @property
    def on_press(self):
        return self._on_press

    @property
    def on_release(self):
        return self._on_release