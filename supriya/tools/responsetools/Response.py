# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Response(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_osc_message',
        )

    _address = None

    ### INITIALIZER ###

    def __init__(
        self,
        osc_message=None,
        ):
        self._osc_message = osc_message

    ### PUBLIC METHODS ###

    def to_dict(self):
        result = {}
        for key, value in self.__getstate__().items():
            key = key[1:]
            if key == 'osc_message':
                continue
            result[key] = value
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def osc_message(self):
        return self._osc_message