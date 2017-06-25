# -*- encoding: utf-8 -*-
import abc
import threading
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Dispatcher(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback_map',
        '_debug',
        '_lock',
        )

    ### INITIALIZER ###

    def __init__(self, debug=False):
        self._callback_map = {}
        self._debug = bool(debug)
        self._lock = threading.RLock()

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        callback_pairs = []
        input_ = self._coerce_input(expr)
        if self.debug:
            print('RECV', type(self))
            for line in repr(input_).splitlines():
                print('    ' + line)
        with self.lock:
            for x in input_:
                callbacks = self._collect_callbacks(x)
                for callback in callbacks:
                    callback_pairs.append((callback, x))
                    if callback.is_one_shot:
                        self._unregister_one_callback(callback)
        for callback, x in callback_pairs:
            callback(x)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _coerce_input(self, expr):
        raise NotImplementedError

    def _collect_callbacks(self, expr):
        callbacks = []
        for callback in self._callback_map.get(None, []):
            if callback not in callbacks:
                if callback.matches(expr):
                    callbacks.append(callback)
        for callback in self._callback_map.get(type(expr), []):
            if callback not in callbacks:
                if callback.matches(expr):
                    callbacks.append(callback)
        return callbacks

    def _unregister_one_callback(self, callback):
        prototype = callback.prototype
        for class_ in prototype:
            if class_ in self._callback_map:
                if callback in self._callback_map[class_]:
                    self._callback_map[class_].remove(callback)
                if not self._callback_map[class_]:
                    del(self._callback_map[class_])

    ### PUBLIC METHODS ###

    def register_callback(self, callback):
        assert isinstance(callback, self.callback_class)
        prototype = callback.prototype
        with self.lock:
            for class_ in prototype:
                if class_ not in self._callback_map:
                    self._callback_map[class_] = []
                self._callback_map[class_].append(callback)

    def unregister_callback(self, callback):
        assert isinstance(callback, self.callback_class)
        with self.lock:
            self._unregister_one_callback(callback)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def callback_class(self):
        return NotImplementedError

    @property
    def debug(self):
        return self._debug

    @property
    def lock(self):
        return self._lock
