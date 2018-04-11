from supriya.tools.ugentools.UGen import UGen


class OutputProxy(UGen):
    """

    ::

        >>> output_proxy = ugentools.OutputProxy.ar(
        ...     index=index,
        ...     its_source_ugen=its_source_ugen,
        ...     rate=rate,
        ...     )
        >>> output_proxy
        OutputProxy.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'rate',
        'its_source_ugen',
        'index',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        index=None,
        its_source_ugen=None,
        rate=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            index=index,
            its_source_ugen=its_source_ugen,
            rate=rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        index=None,
        its_source_ugen=None,
        rate=None,
        ):
        """
        Constructs a OutputProxy.

        ::

            >>> output_proxy = ugentools.OutputProxy.new(
            ...     index=index,
            ...     its_source_ugen=its_source_ugen,
            ...     rate=rate,
            ...     )
            >>> output_proxy
            OutputProxy.new()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            index=index,
            its_source_ugen=its_source_ugen,
            rate=rate,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        """
        Gets `index` input of OutputProxy.

        ::

            >>> output_proxy = ugentools.OutputProxy.ar(
            ...     index=index,
            ...     its_source_ugen=its_source_ugen,
            ...     rate=rate,
            ...     )
            >>> output_proxy.index

        Returns ugen input.
        """
        index = self._ordered_input_names.index('index')
        return self._inputs[index]

    @property
    def its_source_ugen(self):
        """
        Gets `its_source_ugen` input of OutputProxy.

        ::

            >>> output_proxy = ugentools.OutputProxy.ar(
            ...     index=index,
            ...     its_source_ugen=its_source_ugen,
            ...     rate=rate,
            ...     )
            >>> output_proxy.its_source_ugen

        Returns ugen input.
        """
        index = self._ordered_input_names.index('its_source_ugen')
        return self._inputs[index]

    @property
    def rate(self):
        """
        Gets `rate` input of OutputProxy.

        ::

            >>> output_proxy = ugentools.OutputProxy.ar(
            ...     index=index,
            ...     its_source_ugen=its_source_ugen,
            ...     rate=rate,
            ...     )
            >>> output_proxy.rate

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]
