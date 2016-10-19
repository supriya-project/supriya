# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class MidEQ(Filter):
    r"""
    A parametric filter.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> mid_eq = ugentools.MidEQ.ar(
        ...     db=0,
        ...     frequency=440,
        ...     reciprocal_of_q=1,
        ...     source=source,
        ...     )
        >>> mid_eq
        MidEQ.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_of_q',
        'db',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        db=0,
        frequency=440,
        reciprocal_of_q=1,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        db=0,
        frequency=440,
        reciprocal_of_q=1,
        source=None,
        ):
        r"""
        Constructs an audio-rate MidEQ.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> mid_eq = ugentools.MidEQ.ar(
            ...     db=0,
            ...     frequency=440,
            ...     reciprocal_of_q=1,
            ...     source=source,
            ...     )
            >>> mid_eq
            MidEQ.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        db=0,
        frequency=440,
        reciprocal_of_q=1,
        source=None,
        ):
        r"""
        Constructs a control-rate MidEQ.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> mid_eq = ugentools.MidEQ.kr(
            ...     db=0,
            ...     frequency=440,
            ...     reciprocal_of_q=1,
            ...     source=source,
            ...     )
            >>> mid_eq
            MidEQ.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            db=db,
            frequency=frequency,
            reciprocal_of_q=reciprocal_of_q,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def db(self):
        r"""
        Gets `db` input of MidEQ.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> mid_eq = ugentools.MidEQ.ar(
            ...     db=0,
            ...     frequency=440,
            ...     reciprocal_of_q=1,
            ...     source=source,
            ...     )
            >>> mid_eq.db
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('db')
        return self._inputs[index]

    @property
    def frequency(self):
        r"""
        Gets `frequency` input of MidEQ.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> mid_eq = ugentools.MidEQ.ar(
            ...     db=0,
            ...     frequency=440,
            ...     reciprocal_of_q=1,
            ...     source=source,
            ...     )
            >>> mid_eq.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def reciprocal_of_q(self):
        r"""
        Gets `reciprocal_of_q` input of MidEQ.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> mid_eq = ugentools.MidEQ.ar(
            ...     db=0,
            ...     frequency=440,
            ...     reciprocal_of_q=1,
            ...     source=source,
            ...     )
            >>> mid_eq.reciprocal_of_q
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reciprocal_of_q')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of MidEQ.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> mid_eq = ugentools.MidEQ.ar(
            ...     db=0,
            ...     frequency=440,
            ...     reciprocal_of_q=1,
            ...     source=source,
            ...     )
            >>> mid_eq.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
