# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dreset(DUGen):
    r'''

    ::

        >>> dreset = ugentools.Dreset.(
        ...     reset=0,
        ...     source=None,
        ...     )
        >>> dreset

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'reset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        reset=0,
        source=None,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            reset=reset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        reset=0,
        source=None,
        ):
        r'''Constructs a Dreset.

        ::

            >>> dreset = ugentools.Dreset.new(
            ...     reset=0,
            ...     source=None,
            ...     )
            >>> dreset

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            reset=reset,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def reset(self):
        r'''Gets `reset` input of Dreset.

        ::

            >>> dreset = ugentools.Dreset.ar(
            ...     reset=0,
            ...     source=None,
            ...     )
            >>> dreset.reset

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Dreset.

        ::

            >>> dreset = ugentools.Dreset.ar(
            ...     reset=0,
            ...     source=None,
            ...     )
            >>> dreset.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]