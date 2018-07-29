from supriya.ugens.UGen import UGen


class CheckBadValues(UGen):
    """
    Tests for infinity, not-a-number, and denormals.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> ugen_id = 23
        >>> post_mode = 0
        >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
        ...     source=source,
        ...     ugen_id=ugen_id,
        ...     post_mode=post_mode,
        ...     )
        >>> check_bad_values
        CheckBadValues.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'ugen_id',
        'post_mode',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        ugen_id=0,
        post_mode=2,
        source=None,
        ):
        assert int(post_mode) in (0, 1, 2)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        ugen_id=0,
        post_mode=2,
        source=None,
        ):
        """
        Constructs an audio-rate CheckBadValues.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> ugen_id = 23
            >>> post_mode = 0
            >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
            ...     source=source,
            ...     ugen_id=ugen_id,
            ...     post_mode=post_mode,
            ...     )
            >>> check_bad_values
            CheckBadValues.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        ugen_id=0,
        post_mode=2,
        source=None,
        ):
        """
        Constructs a control-rate CheckBadValues.

        ::

            >>> source = supriya.ugens.WhiteNoise.kr()
            >>> ugen_id = 23
            >>> post_mode = 0
            >>> check_bad_values = supriya.ugens.CheckBadValues.kr(
            ...     source=source,
            ...     ugen_id=ugen_id,
            ...     post_mode=post_mode,
            ...     )
            >>> check_bad_values
            CheckBadValues.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            ugen_id=ugen_id,
            post_mode=post_mode,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def post_mode(self):
        """
        Gets `post_mode` input of CheckBadValues.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> ugen_id = 23
            >>> post_mode = 0
            >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
            ...     source=source,
            ...     ugen_id=ugen_id,
            ...     post_mode=post_mode,
            ...     )
            >>> check_bad_values.post_mode
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('post_mode')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of CheckBadValues.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> ugen_id = 23
            >>> post_mode = 0
            >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
            ...     source=source,
            ...     ugen_id=ugen_id,
            ...     post_mode=post_mode,
            ...     )
            >>> check_bad_values.source
            SinOsc.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def ugen_id(self):
        """
        Gets `ugen_id` of CheckBadValues.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> ugen_id = 23
            >>> post_mode = 0
            >>> check_bad_values = supriya.ugens.CheckBadValues.ar(
            ...     source=source,
            ...     ugen_id=ugen_id,
            ...     post_mode=post_mode,
            ...     )
            >>> check_bad_values.ugen_id
            23.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('ugen_id')
        return self._inputs[index]
