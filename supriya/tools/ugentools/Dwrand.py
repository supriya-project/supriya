# -*- encoding: utf-8 -*-
import collections
from supriya.tools.ugentools.DUGen import DUGen


class Dwrand(DUGen):
    r'''A demand-rate weighted random sequence generator.

    ::

        >>> sequence = [0, 1, 2, 7]
        >>> weights = [0.4, 0.4, 0.1, 0.1]
        >>> dwrand = ugentools.Dwrand(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     weights=weights,
        ...     )
        >>> dwrand
        Dwrand()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'repeats',
        'length',
        'weights',
        'sequence',
        )

    _unexpanded_input_names = (
        'weights',
        'sequence',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        repeats=1,
        sequence=None,
        weights=None,
        ):
        if not isinstance(sequence, collections.Sequence):
            sequence = [sequence]
        sequence = tuple(float(_) for _ in sequence)
        if not isinstance(weights, collections.Sequence):
            weights = [weights]
        weights = tuple(float(_) for _ in weights)
        weights = weights[:len(sequence)]
        weights += (0.,) * (len(sequence) - len(weights))
        DUGen.__init__(
            self,
            repeats=repeats,
            length=len(sequence),
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

            >>> sequence = [0, 1, 2, 7]
            >>> weights = [0.4, 0.4, 0.1, 0.1]
            >>> dwrand = ugentools.Dwrand.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     weights=weights,
            ...     )
            >>> dwrand
            Dwrand()

        Returns ugen graph.
        '''
        ugen = cls._new_expanded(
            repeats=repeats,
            sequence=sequence,
            weights=weights,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets `length` input of Dwrand.

        ::

            >>> sequence = [0, 1, 2, 7]
            >>> weights = [0.4, 0.4, 0.1, 0.1]
            >>> dwrand = ugentools.Dwrand(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     weights=weights,
            ...     )
            >>> dwrand.length
            4

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return int(self._inputs[index])

    @property
    def repeats(self):
        r'''Gets `repeats` input of Dwrand.

        ::

            >>> sequence = [0, 1, 2, 7]
            >>> weights = [0.4, 0.4, 0.1, 0.1]
            >>> dwrand = ugentools.Dwrand(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     weights=weights,
            ...     )
            >>> dwrand.repeats
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]

    @property
    def sequence(self):
        r'''Gets `sequence` input of Dwrand.

        ::

            >>> sequence = [0, 1, 2, 7]
            >>> weights = [0.4, 0.4, 0.1, 0.1]
            >>> dwrand = ugentools.Dwrand(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     weights=weights,
            ...     )
            >>> dwrand.sequence
            (0.0, 1.0, 2.0, 7.0)

        Returns ugen input.
        '''
        length = self.length
        index = self._ordered_input_names.index('length') + 1
        return tuple(self._inputs[index + length:index + (length * 2)])

    @property
    def weights(self):
        r'''Gets `weights` input of Dwrand.

        ::

            >>> sequence = [0, 1, 2, 7]
            >>> weights = [0.4, 0.4, 0.1, 0.1]
            >>> dwrand = ugentools.Dwrand(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     weights=weights,
            ...     )
            >>> dwrand.weights
            (0.4, 0.4, 0.1, 0.1)

        Returns ugen input.
        '''
        length = self.length
        index = self._ordered_input_names.index('length') + 1
        return tuple(self._inputs[index:index + length])