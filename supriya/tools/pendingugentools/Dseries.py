# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dseries(DUGen):
    r'''

    ::

        >>> dseries = ugentools.Dseries.ar(
        ...     length="float('inf')",
        ...     start=1,
        ...     step=1,
        ...     )
        >>> dseries
        Dseries.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'start',
        'step',
        'length',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        length="float('inf')",
        start=1,
        step=1,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            length=length,
            start=start,
            step=step,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        length="float('inf')",
        start=1,
        step=1,
        ):
        r'''Constructs a Dseries.

        ::

            >>> dseries = ugentools.Dseries.new(
            ...     length="float('inf')",
            ...     start=1,
            ...     step=1,
            ...     )
            >>> dseries
            Dseries.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            length=length,
            start=start,
            step=step,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets `length` input of Dseries.

        ::

            >>> dseries = ugentools.Dseries.ar(
            ...     length="float('inf')",
            ...     start=1,
            ...     step=1,
            ...     )
            >>> dseries.length

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def start(self):
        r'''Gets `start` input of Dseries.

        ::

            >>> dseries = ugentools.Dseries.ar(
            ...     length="float('inf')",
            ...     start=1,
            ...     step=1,
            ...     )
            >>> dseries.start
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def step(self):
        r'''Gets `step` input of Dseries.

        ::

            >>> dseries = ugentools.Dseries.ar(
            ...     length="float('inf')",
            ...     start=1,
            ...     step=1,
            ...     )
            >>> dseries.step
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('step')
        return self._inputs[index]