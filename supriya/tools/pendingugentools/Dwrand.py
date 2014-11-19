# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dwrand(DUGen):
    r'''

    ::

        >>> dwrand = ugentools.Dwrand.(
        ...     repeats=1,
        ...     sequence=None,
        ...     weights=None,
        ...     )
        >>> dwrand

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'sequence',
        'weights',
        'repeats',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        repeats=1,
        sequence=None,
        weights=None,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            repeats=repeats,
            sequence=sequence,
            weights=weights,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        repeats=1,
        sequence=None,
        weights=None,
        ):
        r'''Constructs a Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.new(
            ...     repeats=1,
            ...     sequence=None,
            ...     weights=None,
            ...     )
            >>> dwrand

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            repeats=repeats,
            sequence=sequence,
            weights=weights,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def repeats(self):
        r'''Gets `repeats` input of Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.ar(
            ...     repeats=1,
            ...     sequence=None,
            ...     weights=None,
            ...     )
            >>> dwrand.repeats

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]

    @property
    def sequence(self):
        r'''Gets `sequence` input of Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.ar(
            ...     repeats=1,
            ...     sequence=None,
            ...     weights=None,
            ...     )
            >>> dwrand.sequence

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('sequence')
        return self._inputs[index]

    @property
    def weights(self):
        r'''Gets `weights` input of Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.ar(
            ...     repeats=1,
            ...     sequence=None,
            ...     weights=None,
            ...     )
            >>> dwrand.weights

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('weights')
        return self._inputs[index]