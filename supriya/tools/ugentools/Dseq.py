# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dseq(DUGen):
    r"""
    A demand-rate sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dseq = ugentools.Dseq.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     )
        >>> dseq
        Dseq()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'repeats',
        'sequence',
        )

    _unexpanded_input_names = (
        'sequence',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        repeats=1,
        sequence=None,
        ):
        DUGen.__init__(
            self,
            repeats=repeats,
            sequence=sequence,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        repeats=1,
        sequence=None,
        ):
        r"""
        Constructs a Dseq.

        ::

            >>> sequence = (1, 2, 3)
            >>> dseq = ugentools.Dseq.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dseq
            Dseq()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            repeats=repeats,
            sequence=sequence,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def repeats(self):
        r"""
        Gets `repeats` input of Dseq.

        ::

            >>> sequence = (1, 2, 3)
            >>> dseq = ugentools.Dseq.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dseq.repeats
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]

    @property
    def sequence(self):
        r"""
        Gets `sequence` input of Dseq.

        ::

            >>> sequence = (1, 2, 3)
            >>> dseq = ugentools.Dseq.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dseq.sequence
            (1.0, 2.0, 3.0)

        Returns ugen input.
        """
        index = self._ordered_input_names.index('sequence')
        return tuple(self._inputs[index:])
