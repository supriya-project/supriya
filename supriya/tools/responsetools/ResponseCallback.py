# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ResponseCallback(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_is_one_shot',
        '_procedure',
        '_response_prototype',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        procedure=None,
        response_prototype=None,
        is_one_shot=False,
        ):
        #from supriya.tools import responsetools
        assert callable(procedure)
        if response_prototype is not None:
            if not isinstance(response_prototype, tuple):
                response_prototype = (response_prototype,)
            #prototype = responsetools.Response
            #assert all(issubclass(x, prototype) for x in response_prototype)
        self._procedure = procedure
        self._response_prototype = response_prototype
        self._is_one_shot = bool(is_one_shot)

    ### SPECIAL METHODS ###

    def __call__(self, message):
        self._procedure(message)

    ### PUBLIC PROPERTIES ###

    @property
    def is_one_shot(self):
        return self._is_one_shot

    @property
    def procedure(self):
        return self._procedure

    @property
    def response_prototype(self):
        return self._response_prototype