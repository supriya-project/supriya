# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Dswitch1 import Dswitch1


class Dswitch(Dswitch1):
    r'''

    ::

        >>> dswitch = ugentools.Dswitch.ar(
        ...     index=index,
        ...     sequence=sequence,
        ...     )
        >>> dswitch
        Dswitch.ar()

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
        Dswitch1.__init__(
            self,
            calculation_rate=calculation_rate,
            index=index,
            sequence=sequence,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        index=None,
        sequence=None,
        ):
        r'''Constructs a Dswitch.

        ::

            >>> dswitch = ugentools.Dswitch.new(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch
            Dswitch.new()

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
        r'''Gets `index` input of Dswitch.

        ::

            >>> dswitch = ugentools.Dswitch.ar(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch.index

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('index')
        return self._inputs[index]

    @property
    def sequence(self):
        r'''Gets `sequence` input of Dswitch.

        ::

            >>> dswitch = ugentools.Dswitch.ar(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch.sequence

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('sequence')
        return self._inputs[index]