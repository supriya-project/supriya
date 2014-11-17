# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiCallback(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_number',
        '_is_one_shot',
        '_procedure',
        '_prototype',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        procedure=None,
        channel_number=None,
        prototype=None,
        is_one_shot=False,
        ):
        assert callable(procedure)
        if channel_number is not None:
            channel_number = int(channel_number)
            assert 0 < channel_number < 16
        if prototype is not None:
            if not isinstance(prototype, tuple):
                prototype = (prototype,)
        assert callable(procedure)
        self._channel_number = channel_number
        self._is_one_shot = bool(is_one_shot)
        self._prototype = prototype
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
    def prototype(self):
        return self._prototype

    @property
    def dispatcher_key(self):
        return (
            self._prototype,
            self._channel_number,
            )