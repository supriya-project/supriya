# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ResponseDispatcher(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback_map',
        '_lock',
        )

    ### INITIALIZER ###

    def __init__(self):
        from supriya.tools import threadtools
        self._lock = threadtools.ReadWriteLock()
        self._callback_map = {}

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        from supriya.tools import responsetools
        if not isinstance(expr, responsetools.Response):
            response = responsetools.ResponseManager.handle_message(expr)
        if not isinstance(response, tuple):
            response = (response,)
        pending_removals = []
        with self.lock.read_access:
            for x in response:
                callbacks = self._callback_map.get(None, [])
                callbacks += self._callback_map.get(type(x), [])
                for callback in callbacks:
                    callback(x)
                    if callback.is_one_shot:
                        pending_removals.append(callback)
        if pending_removals:
            with self.lock.write_access:
                for callback in pending_removals:
                    self.unregister_callback(callback)

    ### PUBLIC METHODS ###

    def register_callback(self, callback):
        from supriya.tools import responsetools
        assert isinstance(callback, responsetools.ResponseCallback)
        response_prototype = callback.response_prototype
        for class_ in response_prototype:
            if class_ not in self._callback_map:
                self._callback_map[class_] = []
            self._callback_map[class_].append(callback)

    def unregister_callback(self, callback):
        from supriya.tools import responsetools
        assert isinstance(callback, responsetools.ResponseCallback)
        response_prototype = callback.response_prototype
        for class_ in response_prototype:
            if class_ in self._callback_map:
                if callback in self._callback_map[class_]:
                    self._callback_map[class_].remove(callback)
                if not self._callback_map[class_]:
                    del(self._callback_map[class_])

    ### PUBLIC PROPERTIES ###

    @property
    def lock(self):
        return self._lock