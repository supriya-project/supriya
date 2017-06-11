# -*- encoding: utf-8 -*-
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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad import new
        super_class = super(SupriyaValueObject, self)
        format_specification = super_class._get_format_specification()
        return new(format_specification, repr_is_indented=False)

    ### PUBLIC PROPERTIES ###

    @property
    def channel_number(self):
        return self._channel_number

    @property
    def dispatcher_key(self):
        return (
            type(self),
            self._channel_number,
            )

    @property
    def timestamp(self):
        return self._timestamp
