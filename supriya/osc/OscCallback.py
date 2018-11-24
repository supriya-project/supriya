from supriya.system.SupriyaObject import SupriyaObject


class OscCallback(SupriyaObject):
    """
    An OSC callback.

    ::

        >>> import supriya.osc
        >>> callback = supriya.osc.OscCallback(
        ...     address_pattern='/*',
        ...     procedure=lambda x: print('GOT:', x),
        ...     )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_address_pattern", "_argument_template", "_is_one_shot", "_procedure")

    ### INITIALIZER ###

    def __init__(
        self,
        address_pattern=None,
        argument_template=None,
        is_one_shot=False,
        procedure=None,
    ):
        self._address_pattern = address_pattern
        if argument_template is not None:
            argument_template = tuple(argument_template)
        self._argument_template = argument_template
        self._procedure = procedure
        self._is_one_shot = bool(is_one_shot)

    ### SPECIAL METHODS ###

    def __call__(self, message):
        self._procedure(message)

    ### PUBLIC PROPERTIES ###

    @property
    def address_pattern(self):
        """
        The address pattern of the callback.

        ::

            >>> callback = supriya.osc.OscCallback(
            ...     address_pattern='/*',
            ...     procedure=lambda x: print('GOT:', x),
            ...     )
            >>> callback.address_pattern
            '/*'

        Returns string.
        """
        return self._address_pattern

    @property
    def argument_template(self):
        return self._argument_template

    @property
    def is_one_shot(self):
        """
        Is true when the callback should be unregistered after being
        called.

        ::

            >>> callback = supriya.osc.OscCallback(
            ...     address_pattern='/*',
            ...     procedure=lambda x: print('GOT:', x),
            ...     )
            >>> callback.is_one_shot
            False

        Returns boolean.
        """
        return self._is_one_shot

    @property
    def procedure(self):
        """
        Gets the procedure to be called.

        Returns callable.
        """
        return self._procedure
