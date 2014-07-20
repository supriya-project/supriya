# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiCallback(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_number',
        '_is_one_shot',
        '_procedure',
        '_midi_prototype',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        procedure=None,
        channel_number=None,
        midi_prototype=None,
        is_one_shot=False,
        ):
        assert callable(procedure)
        if channel_number is not None:
            channel_number = int(channel_number)
            assert 0 < channel_number < 16
        if midi_prototype is not None:
            if not isinstance(midi_prototype, tuple):
                midi_prototype = (midi_prototype,)
        assert callable(procedure)
        self._channel_number = channel_number
        self._is_one_shot = bool(is_one_shot)
        self._midi_prototype = midi_prototype
        self._procedure = procedure

    ### SPECIAL METHODS ###

    def __call__(self, message):
        self._procedure(message)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_number(self):
        return self._channel_number

    @property
    def is_one_shot(self):
        return self._is_one_shot

    @property
    def procedure(self):
        return self._procedure

    @property
    def midi_prototype(self):
        return self._midi_prototype