# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dswitch1(DUGen):
    r'''

    ::

        >>> dswitch_1 = ugentools.Dswitch1.ar(
        ...     index=index,
        ...     sequence=sequence,
        ...     )
        >>> dswitch_1
        Dswitch1.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'sequence',
        'index',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        index=None,
        sequence=None,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            index=index,
            sequence=sequence,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        index=index,
        sequence=sequence,
        ):
        r'''Constructs a Dswitch1.

        ::

            >>> dswitch_1 = ugentools.Dswitch1.new(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch_1
            Dswitch1.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            index=index,
            sequence=sequence,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''Gets `index` input of Dswitch1.

        ::

            >>> dswitch_1 = ugentools.Dswitch1.ar(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch_1.index

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('index')
        return self._inputs[index]

    @property
    def sequence(self):
        r'''Gets `sequence` input of Dswitch1.

        ::

            >>> dswitch_1 = ugentools.Dswitch1.ar(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch_1.sequence

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('sequence')
        return self._inputs[index]