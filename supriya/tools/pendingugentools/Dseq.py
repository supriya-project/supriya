# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.ListDUGen import ListDUGen


class Dseq(ListDUGen):
    r'''

    ::

        >>> dseq = ugentools.Dseq.(
        ...     list=None,
        ...     repeats=1,
        ...     )
        >>> dseq

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
        r'''Constructs a Dseq.

        ::

            >>> dseq = ugentools.Dseq.new(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> dseq

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
        r'''Gets `list` input of Dseq.

        ::

            >>> dseq = ugentools.Dseq.ar(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> dseq.list

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('list')
        return self._inputs[index]

    @property
    def repeats(self):
        r'''Gets `repeats` input of Dseq.

        ::

            >>> dseq = ugentools.Dseq.ar(
            ...     list=None,
            ...     repeats=1,
            ...     )
            >>> dseq.repeats

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]