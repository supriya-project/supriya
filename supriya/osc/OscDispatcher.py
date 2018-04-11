import re
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class OscDispatcher(SupriyaObject):
    """
    An OSC message dispatcher.

    ::

        >>> import supriya.osc
        >>> dispatcher = supriya.osc.OscDispatcher()

    ::

        >>> osc_callback = supriya.osc.OscCallback(
        ...     address_pattern='/*',
        ...     procedure=lambda x: print('GOT:', x),
        ...     )
        >>> dispatcher.register_callback(osc_callback)

    ::

        >>> message = supriya.osc.OscMessage('/okay', 1, 2, 3)
        >>> dispatcher(message)
        GOT: size 28
           0   2f 6f 6b 61  79 00 00 00  2c 69 69 69  00 00 00 00   |/okay...,iii....|
          16   00 00 00 01  00 00 00 02  00 00 00 03                |............|

    ::

        >>> dispatcher.unregister_callback(osc_callback)
        >>> dispatcher(message)

    """

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
        """
        Handles `message`.

        Finds all matching callbacks and passes the message to each.

        Returns none.
        """
        import supriya.osc
        assert isinstance(message, supriya.osc.OscMessage)
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

    def register_callback(self, osc_callback):
        """
        Registers `osc_callback`.

        Returns none.
        """
        import supriya.osc
        assert isinstance(osc_callback, supriya.osc.OscCallback)
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

    def unregister_callback(self, osc_callback):
        """
        Unregisters `osc_callback`.

        Returns none.
        """
        import supriya.osc
        assert isinstance(osc_callback, supriya.osc.OscCallback)
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
