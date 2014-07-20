# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class MidiMessage(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_number',
        '_timestamp',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        timestamp=None,
        ):
        self._channel_number = channel_number
        self._timestamp = timestamp

    ### PUBLIC PROPERTIES ###

    @property
    def channel_number(self):
        return self._channel_number

    @property
    def timestamp(self):
        return self._timestamp