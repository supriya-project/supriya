# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class ListDUGen(DUGen):
    r'''

    ::

        >>> list_dugen = ugentools.ListDUGen.ar(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     )
        >>> list_dugen
        ListDUGen.ar()

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
        DUGen.__init__(
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
        r'''Constructs a ListDUGen.

        ::

            >>> list_dugen = ugentools.ListDUGen.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> list_dugen
            ListDUGen.new()

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
        r'''Gets `repeats` input of ListDUGen.

        ::

            >>> list_dugen = ugentools.ListDUGen.ar(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> list_dugen.repeats
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]

    @property
    def sequence(self):
        r'''Gets `sequence` input of ListDUGen.

        ::

            >>> list_dugen = ugentools.ListDUGen.ar(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> list_dugen.sequence

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('sequence')
        return self._inputs[index]