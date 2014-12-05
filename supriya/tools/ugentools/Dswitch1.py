# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dswitch1(DUGen):
    r'''A demand-rate generator for switching between inputs.

    ::

        >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
        >>> sequence = (1., 2., 3.)
        >>> dswitch_1 = ugentools.Dswitch1(
        ...     index=index,
        ...     sequence=sequence,
        ...     )
        >>> dswitch_1
        Dswitch1()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'index',
        'sequence',
        )

    _unexpanded_input_names = (
        'sequence',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        index=None,
        sequence=None,
        ):
        DUGen.__init__(
            self,
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
        r'''Constructs a Dswitch1.

        ::

            >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
            >>> sequence = (1., 2., 3.)
            >>> dswitch_1 = ugentools.Dswitch1.new(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch_1
            Dswitch1()

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            index=index,
            sequence=sequence,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''Gets `index` input of Dswitch1.

        ::

            >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
            >>> sequence = (1., 2., 3.)
            >>> dswitch_1 = ugentools.Dswitch1(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch_1.index
            OutputProxy(
                source=Dseq(
                    repeats=1.0,
                    sequence=(0.0, 1.0, 2.0, 1.0, 0.0)
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('index')
        return self._inputs[index]

    @property
    def sequence(self):
        r'''Gets `sequence` input of Dswitch1.

        ::

            >>> index = ugentools.Dseq(sequence=[0, 1, 2, 1, 0])
            >>> sequence = (1., 2., 3.)
            >>> dswitch_1 = ugentools.Dswitch1(
            ...     index=index,
            ...     sequence=sequence,
            ...     )
            >>> dswitch_1.sequence
            (1.0, 2.0, 3.0)

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('index') + 1
        return tuple(self._inputs[index:])