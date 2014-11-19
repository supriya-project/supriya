# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dwrand(DUGen):
    r'''

    ::

        >>> dwrand = ugentools.Dwrand.(
        ...     list=None,
        ...     repeats=1,
        ...     weights=None,
        ...     )
        >>> dwrand

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'list',
        'weights',
        'repeats',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        list=None,
        repeats=1,
        weights=None,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            list=list,
            repeats=repeats,
            weights=weights,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        list=None,
        repeats=1,
        weights=None,
        ):
        r'''Constructs a Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.new(
            ...     list=None,
            ...     repeats=1,
            ...     weights=None,
            ...     )
            >>> dwrand

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            list=list,
            repeats=repeats,
            weights=weights,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def list(self):
        r'''Gets `list` input of Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.ar(
            ...     list=None,
            ...     repeats=1,
            ...     weights=None,
            ...     )
            >>> dwrand.list

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('list')
        return self._inputs[index]

    @property
    def repeats(self):
        r'''Gets `repeats` input of Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.ar(
            ...     list=None,
            ...     repeats=1,
            ...     weights=None,
            ...     )
            >>> dwrand.repeats

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]

    @property
    def weights(self):
        r'''Gets `weights` input of Dwrand.

        ::

            >>> dwrand = ugentools.Dwrand.ar(
            ...     list=None,
            ...     repeats=1,
            ...     weights=None,
            ...     )
            >>> dwrand.weights

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('weights')
        return self._inputs[index]