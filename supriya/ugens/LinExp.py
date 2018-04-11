from supriya.ugens.PureUGen import PureUGen


class LinExp(PureUGen):
    """
    A linear-to-exponential range mapper.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> lin_exp = supriya.ugens.LinExp.ar(
        ...     input_maximum=1.0,
        ...     input_minimum=-1.0,
        ...     output_maximum=22050,
        ...     output_minimum=20,
        ...     source=source,
        ...     )
        >>> lin_exp
        LinExp.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'input_minimum',
        'input_maximum',
        'output_minimum',
        'output_maximum',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        input_maximum=1,
        input_minimum=0,
        output_maximum=2,
        output_minimum=1,
        source=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            input_maximum=input_maximum,
            input_minimum=input_minimum,
            output_maximum=output_maximum,
            output_minimum=output_minimum,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        input_maximum=1,
        input_minimum=0,
        output_maximum=2,
        output_minimum=1,
        source=None,
        ):
        """
        Constructs an audio-rate linear-to-exponential range mapper.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> lin_exp = supriya.ugens.LinExp.ar(
            ...     input_maximum=1.0,
            ...     input_minimum=-1.0,
            ...     output_maximum=22050,
            ...     output_minimum=20,
            ...     source=source,
            ...     )
            >>> lin_exp
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input_maximum=input_maximum,
            input_minimum=input_minimum,
            output_maximum=output_maximum,
            output_minimum=output_minimum,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        input_maximum=1,
        input_minimum=0,
        output_maximum=2,
        output_minimum=1,
        source=0,
        ):
        """
        Constructs a control-rate linear-to-exponential range mapper.

        ::

            >>> source = supriya.ugens.SinOsc.kr(frequency=[4, 2])
            >>> lin_exp = supriya.ugens.LinExp.kr(
            ...     input_maximum=1.0,
            ...     input_minimum=-1.0,
            ...     output_maximum=22050,
            ...     output_minimum=20,
            ...     source=source,
            ...     )
            >>> lin_exp
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input_maximum=input_maximum,
            input_minimum=input_minimum,
            output_maximum=output_maximum,
            output_minimum=output_minimum,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def input_maximum(self):
        """
        Gets `input_maximum` input of LinExp.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> lin_exp = supriya.ugens.LinExp.ar(
            ...     input_maximum=1.0,
            ...     input_minimum=-1.0,
            ...     output_maximum=22050,
            ...     output_minimum=20,
            ...     source=source,
            ...     )
            >>> lin_exp.input_maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('input_maximum')
        return self._inputs[index]

    @property
    def input_minimum(self):
        """
        Gets `input_minimum` input of LinExp.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> lin_exp = supriya.ugens.LinExp.ar(
            ...     input_maximum=1.0,
            ...     input_minimum=-1.0,
            ...     output_maximum=22050,
            ...     output_minimum=20,
            ...     source=source,
            ...     )
            >>> lin_exp.input_minimum
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('input_minimum')
        return self._inputs[index]

    @property
    def output_maximum(self):
        """
        Gets `output_maximum` input of LinExp.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> lin_exp = supriya.ugens.LinExp.ar(
            ...     input_maximum=1.0,
            ...     input_minimum=-1.0,
            ...     output_maximum=22050,
            ...     output_minimum=20,
            ...     source=source,
            ...     )
            >>> lin_exp.output_maximum
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('output_maximum')
        return self._inputs[index]

    @property
    def output_minimum(self):
        """
        Gets `output_minimum` input of LinExp.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> lin_exp = supriya.ugens.LinExp.ar(
            ...     input_maximum=1.0,
            ...     input_minimum=-1.0,
            ...     output_maximum=22050,
            ...     output_minimum=20,
            ...     source=source,
            ...     )
            >>> lin_exp.output_minimum
            20.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('output_minimum')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of LinExp.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> lin_exp = supriya.ugens.LinExp.ar(
            ...     input_maximum=1.0,
            ...     input_minimum=-1.0,
            ...     output_maximum=22050,
            ...     output_minimum=20,
            ...     source=source,
            ...     )
            >>> lin_exp.source
            SinOsc.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
