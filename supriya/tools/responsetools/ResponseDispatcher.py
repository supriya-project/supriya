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

    def __call__(self, expr):
        from supriya.tools import responsetools
        if not isinstance(expr, responsetools.Response):
            response = responsetools.ResponseManager.handle_message(expr)
        if not isinstance(response, tuple):
            response = (response,)
        for x in response:
            callbacks = self._response_map.get(None, [])
            callbacks += self._response_map.get(type(x), [])
            for callback in callbacks:
                callback(x)
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