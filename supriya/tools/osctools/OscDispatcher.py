# -*- encoding: utf-8 -*-
from __future__ import print_function
import re
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class OscDispatcher(SupriyaObject):
    r'''An OSC message dispatcher.

    ::

        >>> from supriya import osctools
        >>> dispatcher = osctools.OscDispatcher()

    ::

        >>> osc_callback = osctools.OscCallback(
        ...     address_pattern='/*',
        ...     procedure=lambda x: print('GOT:', x),
        ...     )
        >>> dispatcher.register_osc_callback(osc_callback)

    ::

        >>> message = osctools.OscMessage('/okay', 1, 2, 3)
        >>> dispatcher(message)
        GOT: OscMessage('/okay', 1, 2, 3)

    ::

        >>> dispatcher.unregister_osc_callback(osc_callback)
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
        from supriya.tools import osctools
        assert isinstance(message, osctools.OscMessage)
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
                self.unregister_osc_callback(callback)

    ### PUBLIC METHODS ###

    @staticmethod
    def compile_address_pattern(pattern):
        pattern = pattern.replace('.', '\.')
        pattern = pattern.replace('*', '[.\w|\+]*')
        pattern += '$'
        pattern = re.compile(pattern)
        return pattern

    def register_osc_callback(self, osc_callback):
        r'''Registers `osc_callback`.

        Returns none.
        '''
        from supriya.tools import osctools
        assert isinstance(osc_callback, osctools.OscCallback)
        if osc_callback.address_pattern in self._address_map:
            regex = self._address_map[osc_callback.address_pattern]
        else:
            regex = self.compile_address_pattern(osc_callback.address_pattern)
            self._address_map[osc_callback.address_pattern] = regex
        if regex not in self._regex_map:
            self._regex_map[regex] = []
        osc_callbacks = self._regex_map[regex]
        if osc_callback not in osc_callbacks:
            osc_callbacks.append(osc_callback)

    def unregister_osc_callback(self, osc_callback):
        r'''Unregisters `osc_callback`.

        Returns none.
        '''
        from supriya.tools import osctools
        assert isinstance(osc_callback, osctools.OscCallback)
        if osc_callback.address_pattern not in self._address_map:
            return
        regex = self._address_map[osc_callback.address_pattern]
        if regex not in self._regex_map:
            return
        osc_callbacks = self._regex_map[regex]
        if osc_callback not in osc_callbacks:
            return
        osc_callbacks.remove(osc_callback)
        if not osc_callbacks:
            del(self._regex_map[regex])
            del(self._address_map[osc_callback.address_pattern])