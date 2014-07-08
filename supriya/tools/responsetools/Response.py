# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Response(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_osc_message',
        )

    _address = None
    _request_prototype = None

    ### INITIALIZER ###

    def __init__(
        self,
        osc_message=None,
        ):
        self._osc_message = osc_message

    ### PUBLIC PROPERTIES ###

    @property
    def osc_message(self):
        return self._osc_message