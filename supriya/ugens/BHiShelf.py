from supriya.ugens.BEQSuite import BEQSuite


class BHiShelf(BEQSuite):
    """
    A high-shelf filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
        ...     gain=0,
        ...     frequency=1200,
        ...     reciprocal_of_s=1,
        ...     source=source,
        ...     )
        >>> bhi_shelf
        BHiShelf.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_of_s',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        gain=0,
        frequency=1200,
        reciprocal_of_s=1,
        source=None,
        ):
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            gain=gain,
            frequency=frequency,
            reciprocal_of_s=reciprocal_of_s,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        gain=0,
        frequency=1200,
        reciprocal_of_s=1,
        source=None,
        ):
        """
        Constructs an audio-rate BHiShelf.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
            ...     gain=0,
            ...     frequency=1200,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> bhi_shelf
            BHiShelf.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            gain=gain,
            frequency=frequency,
            reciprocal_of_s=reciprocal_of_s,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def sc(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def gain(self):
        """
        Gets `gain` input of BHiShelf.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
            ...     gain=0,
            ...     frequency=1200,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> bhi_shelf.gain
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of BHiShelf.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
            ...     gain=0,
            ...     frequency=1200,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> bhi_shelf.frequency
            1200.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_s(self):
        """
        Gets `reciprocal_of_s` input of BHiShelf.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
            ...     gain=0,
            ...     frequency=1200,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> bhi_shelf.reciprocal_of_s
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reciprocal_of_s')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of BHiShelf.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> bhi_shelf = supriya.ugens.BHiShelf.ar(
            ...     gain=0,
            ...     frequency=1200,
            ...     reciprocal_of_s=1,
            ...     source=source,
            ...     )
            >>> bhi_shelf.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
