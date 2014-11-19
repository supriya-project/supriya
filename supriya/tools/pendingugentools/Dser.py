# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ListDUGen import ListDUGen


class Dser(ListDUGen):
    r'''

    ::

        >>> dser = ugentools.Dser.(
        ...     list=None,
        ...     repeats=1,
        ...     )
        >>> dser

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'list',
        'repeats',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        list=None,
        repeats=1,
        ):
        ListDUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            list=list,
            repeats=repeats,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        list=None,
        repeats=1,
        ):
        r'''Constructs a Dser.

        ::

            >>> dser = ugentools.Dser.new(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> dser

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            list=list,
            repeats=repeats,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def list(self):
        r'''Gets `list` input of Dser.

        ::

            >>> dser = ugentools.Dser.ar(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> dser.list

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('list')
        return self._inputs[index]

    @property
    def repeats(self):
        r'''Gets `repeats` input of Dser.

        ::

            >>> dser = ugentools.Dser.ar(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> dser.repeats

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]