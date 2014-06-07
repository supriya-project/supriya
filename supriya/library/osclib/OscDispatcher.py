# -*- encoding: utf-8 -*-
from __future__ import print_function
import re


class OscDispatcher(object):
    r'''An OSC message dispatcher.

    ::

        >>> from supriya import osclib
        >>> dispatcher = osclib.OscDispatcher()

    ::

        >>> callback = osclib.OscCallback(
        ...     address_pattern='/*',
        ...     procedure=lambda x: print('GOT:', x),
        ...     )
        >>> dispatcher.register_callback(callback)

    ::

        >>> message = osclib.OscMessage('/okay', 1, 2, 3)
        >>> dispatcher(message)
        GOT: OscMessage('/okay', 1, 2, 3)

    ::

        >>> dispatcher.unregister_callback(callback)
        >>> dispatcher(message)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_address_map',
        '_regex_map',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._address_map = {}
        self._regex_map = {}

    ### SPECIAL METHODS ###

    def __call__(self, message):
        r'''Handles `message`.

        Finds all matching callbacks and passes the message to each.

        Returns none.
        '''
        from supriya.library import osclib
        assert isinstance(message, osclib.OscMessage)
        callbacks = []
        for regex in self._regex_map:
            if regex.match(message.address):
                callbacks.extend(self._regex_map[regex])
        for callback in callbacks:
            if callback.argument_template:
                is_valid = True
                generator = zip(message.contents, callback.argument_template)
                for one, two in generator:
                    if one != two:
                        is_valid = False
                        break
                if not is_valid:
                    continue
            callback(message)
            if callback.is_one_shot:
                self.unregister_callback(callback)

    ### PUBLIC METHODS ###

    @staticmethod
    def compile_address_pattern(pattern):
        pattern = pattern.replace('.', '\.')
        pattern = pattern.replace('*', '[.\w|\+]*')
        pattern += '$'
        pattern = re.compile(pattern)
        return pattern

    def register_callback(self, callback):
        r'''Registers `callback`.

        Returns none.
        '''
        from supriya.library import osclib
        assert isinstance(callback, osclib.OscCallback)
        if callback.address_pattern in self._address_map:
            regex = self._address_map[callback.address_pattern]
        else:
            regex = self.compile_address_pattern(callback.address_pattern)
            self._address_map[callback.address_pattern] = regex
        if regex not in self._regex_map:
            self._regex_map[regex] = []
        callbacks = self._regex_map[regex]
        if callback not in callbacks:
            callbacks.append(callback)

    def unregister_callback(self, callback):
        r'''Unregisters `callback`.

        Returns none.
        '''
        from supriya.library import osclib
        assert isinstance(callback, osclib.OscCallback)
        if callback.address_pattern not in self._address_map:
            return
        regex = self._address_map[callback.address_pattern]
        if regex not in self._regex_map:
            return
        callbacks = self._regex_map[regex]
        if callback not in callbacks:
            return
        callbacks.remove(callback)
        if not callbacks:
            del(self._regex_map[regex])
            del(self._address_map[callback.address_pattern])
