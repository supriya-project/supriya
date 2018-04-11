from supriya.ugens.UGen import UGen


class KeyState(UGen):
    """

    ::

        >>> key_state = supriya.ugens.KeyState.ar(
        ...     keycode=0,
        ...     lag=0.2,
        ...     maxval=1,
        ...     minval=0,
        ...     )
        >>> key_state
        KeyState.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'keycode',
        'minval',
        'maxval',
        'lag',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        keycode=0,
        lag=0.2,
        maxval=1,
        minval=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            keycode=keycode,
            lag=lag,
            maxval=maxval,
            minval=minval,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        keycode=0,
        lag=0.2,
        maxval=1,
        minval=0,
        ):
        """
        Constructs a control-rate KeyState.

        ::

            >>> key_state = supriya.ugens.KeyState.kr(
            ...     keycode=0,
            ...     lag=0.2,
            ...     maxval=1,
            ...     minval=0,
            ...     )
            >>> key_state
            KeyState.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            keycode=keycode,
            lag=lag,
            maxval=maxval,
            minval=minval,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def keycode(self):
        """
        Gets `keycode` input of KeyState.

        ::

            >>> key_state = supriya.ugens.KeyState.ar(
            ...     keycode=0,
            ...     lag=0.2,
            ...     maxval=1,
            ...     minval=0,
            ...     )
            >>> key_state.keycode
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('keycode')
        return self._inputs[index]

    @property
    def lag(self):
        """
        Gets `lag` input of KeyState.

        ::

            >>> key_state = supriya.ugens.KeyState.ar(
            ...     keycode=0,
            ...     lag=0.2,
            ...     maxval=1,
            ...     minval=0,
            ...     )
            >>> key_state.lag
            0.2

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lag')
        return self._inputs[index]

    @property
    def maxval(self):
        """
        Gets `maxval` input of KeyState.

        ::

            >>> key_state = supriya.ugens.KeyState.ar(
            ...     keycode=0,
            ...     lag=0.2,
            ...     maxval=1,
            ...     minval=0,
            ...     )
            >>> key_state.maxval
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maxval')
        return self._inputs[index]

    @property
    def minval(self):
        """
        Gets `minval` input of KeyState.

        ::

            >>> key_state = supriya.ugens.KeyState.ar(
            ...     keycode=0,
            ...     lag=0.2,
            ...     maxval=1,
            ...     minval=0,
            ...     )
            >>> key_state.minval
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minval')
        return self._inputs[index]
