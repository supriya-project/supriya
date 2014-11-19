# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dstutter(DUGen):
    r'''

    ::

        >>> dstutter = ugentools.Dstutter.(
        ...     n=None,
        ...     source=None,
        ...     )
        >>> dstutter

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'n',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        n=None,
        source=None,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            n=n,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        n=None,
        source=None,
        ):
        r'''Constructs a Dstutter.

        ::

            >>> dstutter = ugentools.Dstutter.new(
            ...     n=None,
            ...     source=None,
            ...     )
            >>> dstutter

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            n=n,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def n(self):
        r'''Gets `n` input of Dstutter.

        ::

            >>> dstutter = ugentools.Dstutter.ar(
            ...     n=None,
            ...     source=None,
            ...     )
            >>> dstutter.n

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('n')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Dstutter.

        ::

            >>> dstutter = ugentools.Dstutter.ar(
            ...     n=None,
            ...     source=None,
            ...     )
            >>> dstutter.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]