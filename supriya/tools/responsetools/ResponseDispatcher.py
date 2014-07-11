# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ResponseDispatcher(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_response_map',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._response_map = {}

    ### SPECIAL METHODS ###

    def __call__(self, response):
        callbacks = self._response_map.get(None)
        callbacks += self._response_map.get(type(response), [])
        for callback in callbacks:
            callback(response)
            if callback.is_one_shot:
                self.unregister_callback(callback)

    ### PUBLIC METHODS ###

    def register_callback(self, callback):
        from supriya.tools import responsetools
        assert isinstance(callback, responsetools.ResponseCallback)
        response_prototype = callback.response_prototype
        for class_ in response_prototype:
            if class_ not in self._response_map:
                self._response_map[class_] = []
            self._response_map[class_].append(callback)

    def unregister_callback(self, callback):
        from supriya.tools import responsetools
        assert isinstance(callback, responsetools.ResponseCallback)
        response_prototype = callback.response_prototype
        for class_ in response_prototype:
            if class_ in self._response_map:
                if callback in self._response_map[class_]:
                    self._response_map[class_].remove(callback)
                if not self._response_map[class_]:
                    del(self._response_map[class_])