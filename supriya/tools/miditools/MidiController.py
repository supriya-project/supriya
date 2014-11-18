# -*- encoding: utf-8- -*-
from supriya.tools.bindingtools.BindingSource import BindingSource
from supriya.tools.miditools.MidiCallback import MidiCallback


class MidiController(MidiCallback, BindingSource):
    r'''A MIDI controller change callback.

    ::

        >>> callback = miditools.MidiController(
        ...     channel_number=1,
        ...     controller_number=17,
        ...     )

    ::

        >>> dispatcher = miditools.MidiDispatcher()
        >>> dispatcher.register_callback(callback)
        >>> dispatcher.unregister_callback(callback)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_binding_targets',
        '_controller_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        controller_number=None,
        ):
        from supriya.tools import miditools
        BindingSource.__init__(self)
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
        self._send_bound_event(message.controller_value)

    ### PUBLIC PROPERTIES ###

    @property
    def controller_number(self):
        r'''Gets callback controller number.

        ::

            >>> callback.controller_number
            17

        Returns integer or none.
        '''
        return self._controller_number

    @property
    def dispatcher_key(self):
        r'''Gets callback dispatcher key.

        ::

            >>> callback.dispatcher_key
            (<class 'supriya.tools.miditools.ControllerChangeMessage.ControllerChangeMessage'>, 1, 17)

        Returns tuple.
        '''
        return (
            self._prototype,
            self._channel_number,
            self._controller_number,
            )