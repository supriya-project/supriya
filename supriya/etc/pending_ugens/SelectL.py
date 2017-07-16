from supriya.tools.ugentools.UGen import UGen


class SelectL(UGen):
    """

    ::

        >>> select_l = ugentools.SelectL.ar(
        ...     array=array,
        ...     which=which,
        ...     )
        >>> select_l
        SelectL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'which',
        'array',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        array=None,
        which=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        array=None,
        which=None,
        ):
        """
        Constructs an audio-rate SelectL.

        ::

            >>> select_l = ugentools.SelectL.ar(
            ...     array=array,
            ...     which=which,
            ...     )
            >>> select_l
            SelectL.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )
        return ugen

    # def arSwitch(): ...

    @classmethod
    def kr(
        cls,
        array=None,
        which=None,
        ):
        """
        Constructs a control-rate SelectL.

        ::

            >>> select_l = ugentools.SelectL.kr(
            ...     array=array,
            ...     which=which,
            ...     )
            >>> select_l
            SelectL.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            array=array,
            which=which,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def array(self):
        """
        Gets `array` input of SelectL.

        ::

            >>> select_l = ugentools.SelectL.ar(
            ...     array=array,
            ...     which=which,
            ...     )
            >>> select_l.array

        Returns ugen input.
        """
        index = self._ordered_input_names.index('array')
        return self._inputs[index]

    @property
    def which(self):
        """
        Gets `which` input of SelectL.

        ::

            >>> select_l = ugentools.SelectL.ar(
            ...     array=array,
            ...     which=which,
            ...     )
            >>> select_l.which

        Returns ugen input.
        """
        index = self._ordered_input_names.index('which')
        return self._inputs[index]
