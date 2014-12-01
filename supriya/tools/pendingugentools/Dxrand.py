# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ListDUGen import ListDUGen


class Dxrand(ListDUGen):
    r'''

    ::

        >>> dxrand = ugentools.Dxrand.ar(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     )
        >>> dxrand
        Dxrand.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'sequence',
        'repeats',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        repeats=1,
        sequence=None,
        ):
        ListDUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            repeats=repeats,
            sequence=sequence,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        repeats=1,
        sequence=sequence,
        ):
        r'''Constructs a Dxrand.

        ::

            >>> dxrand = ugentools.Dxrand.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dxrand
            Dxrand.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            repeats=repeats,
            sequence=sequence,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def repeats(self):
        r'''Gets `repeats` input of Dxrand.

        ::

            >>> dxrand = ugentools.Dxrand.ar(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dxrand.repeats
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]

    @property
    def sequence(self):
        r'''Gets `sequence` input of Dxrand.

        ::

            >>> dxrand = ugentools.Dxrand.ar(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dxrand.sequence

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('sequence')
        return self._inputs[index]