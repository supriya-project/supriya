# -*- encoding: utf-8 -*-


class OscCallback(object):
    r'''An OSC callback.

    ::

        >>> from supriya import osclib
        >>> callback = osclib.OscCallback('/*', lambda x: print('GOT:', x))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_address_pattern',
        '_is_one_shot',
        '_procedure',
        )

    ### INITIALIZER ###

    def __init__(self, address_pattern, procedure, is_one_shot=False):
        self._address_pattern = address_pattern
        self._procedure = procedure
        self._is_one_shot = bool(is_one_shot)

    ### SPECIAL METHODS ###

    def __call__(self, message):
        self._procedure(message)

    ### PUBLIC PROPERTIES ###

    @property
    def address_pattern(self):
        r'''The address pattern of the callback.

        ::

            >>> callback.address_pattern
            '/*'

        Returns string.
        '''
        return self._address_pattern

    @property
    def is_one_shot(self):
        r'''Is true when the callback should be unregistered after being
        called.

        ::

            >>> callback.is_one_shot
            False

        Returns boolean.
        '''
        return self._is_one_shot

    @property
    def procedure(self):
        r'''Gets the procedure to be called.

        Returns callable.
        '''
        return self._procedure
