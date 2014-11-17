# -*- encoding: utf-8- -*-
from supriya.tools.miditools.MidiCallback import MidiCallback


class MidiControl(MidiCallback):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_controller_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        controller_number=None,
        ):
        from supriya.tools import miditools
        MidiCallback.__init__(
            self,
            channel_number=channel_number,
            prototype=miditools.ControllerChangeMessage,
            )
        if controller_number is not None:
            controller_number = int(controller_number)
        self._controller_number = controller_number

    ### SPECIAL METHODS ###

    def __call__(self, message):
        print(message)

    ### PUBLIC PROPERTIES ###

    @property
    def controller_number(self):
        return self._controller_number

    @property
    def dispatcher_key(self):
        return (
            self._prototype,
            self._channel_number,
            self._controller_number,
            )