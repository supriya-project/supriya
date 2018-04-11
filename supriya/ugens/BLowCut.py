from supriya.ugens.BHiCut import BHiCut


class BLowCut(BHiCut):
    """
    A low-cut filter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> blow_cut = supriya.ugens.BLowCut.ar(
        ...     frequency=1200,
        ...     max_order=5,
        ...     order=2,
        ...     source=source,
        ...     )
        >>> blow_cut
        BLowCut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'order',
        'max_order',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=1200,
        max_order=5,
        order=2,
        source=None,
        ):
        BHiCut.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )

    ### PUBLIC METHODS ###

    # def allRQs(): ...

    @classmethod
    def ar(
        cls,
        frequency=1200,
        max_order=5,
        order=2,
        source=None,
        ):
        """
        Constructs an audio-rate BLowCut.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> blow_cut = supriya.ugens.BLowCut.ar(
            ...     frequency=1200,
            ...     max_order=5,
            ...     order=2,
            ...     source=source,
            ...     )
            >>> blow_cut
            BLowCut.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    # def filterClass(): ...

    # def initClass(): ...

    @classmethod
    def kr(
        cls,
        frequency=1200,
        max_order=5,
        order=2,
        source=None,
        ):
        """
        Constructs a control-rate BLowCut.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> blow_cut = supriya.ugens.BLowCut.kr(
            ...     frequency=1200,
            ...     max_order=5,
            ...     order=2,
            ...     source=source,
            ...     )
            >>> blow_cut
            BLowCut.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            max_order=max_order,
            order=order,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def new1(): ...

    # def newFixed(): ...

    # def newVari(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of BLowCut.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> blow_cut = supriya.ugens.BLowCut.ar(
            ...     frequency=1200,
            ...     max_order=5,
            ...     order=2,
            ...     source=source,
            ...     )
            >>> blow_cut.frequency
            1200.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def max_order(self):
        """
        Gets `max_order` input of BLowCut.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> blow_cut = supriya.ugens.BLowCut.ar(
            ...     frequency=1200,
            ...     max_order=5,
            ...     order=2,
            ...     source=source,
            ...     )
            >>> blow_cut.max_order
            5.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('max_order')
        return self._inputs[index]

    @property
    def order(self):
        """
        Gets `order` input of BLowCut.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> blow_cut = supriya.ugens.BLowCut.ar(
            ...     frequency=1200,
            ...     max_order=5,
            ...     order=2,
            ...     source=source,
            ...     )
            >>> blow_cut.order
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('order')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of BLowCut.

        ::

            >>> source = supriya.ugens.In.ar(0)
            >>> blow_cut = supriya.ugens.BLowCut.ar(
            ...     frequency=1200,
            ...     max_order=5,
            ...     order=2,
            ...     source=source,
            ...     )
            >>> blow_cut.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
