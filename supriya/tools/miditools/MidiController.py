# -*- encoding: utf-8- -*-
from supriya.tools import bindingtools
from supriya.tools.bindingtools.BindingSource import BindingSource
from supriya.tools.miditools.MidiCallback import MidiCallback


class MidiController(MidiCallback, BindingSource):
    """
    A MIDI controller change callback.

    ::

        >>> callback = miditools.MidiController(
        ...     channel_number=1,
        ...     controller_number=17,
        ...     )

    ::

        >>> dispatcher = miditools.MidiDispatcher()
        >>> dispatcher.register_callback(callback)
        >>> dispatcher.unregister_callback(callback)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_binding_targets',
        '_controller_number',
        '_on_change',
        '_output_range',
        '_previous_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        controller_number=None,
        ):
        from supriya.tools import miditools
        BindingSource.__init__(
            self,
            )
        MidiCallback.__init__(
            self,
            channel_number=channel_number,
            prototype=miditools.ControllerChangeMessage,
            )
        if controller_number is not None:
            controller_number = int(controller_number)
        self._controller_number = controller_number
        self._on_change = bindingtools.BindingInput()
        self._previous_value = None

    ### SPECIAL METHODS ###

    def __call__(self, message):
        value = message.controller_value
        self._send_bound_event(message.controller_value)
        if value != self._previous_value:
            self._on_change._send_bound_event(value)
        self._previous_value = value

    ### PUBLIC PROPERTIES ###

    @property
    def controller_number(self):
        """
        Gets callback controller number.

        ::

            >>> callback.controller_number
            17

        Returns integer or none.
        """
        return self._controller_number

    @property
    def dispatcher_key(self):
        """
        Gets callback dispatcher key.

        ::

            >>> callback.dispatcher_key
            (<class 'supriya.tools.miditools.ControllerChangeMessage.ControllerChangeMessage'>, 1, 17)

        Returns tuple.
        """
        return (
            self._prototype,
            self._channel_number,
            self._controller_number,
            )

    @property
    def on_change(self):
        return self._on_change

    @property
    def previous_value(self):
        return self._previous_value
