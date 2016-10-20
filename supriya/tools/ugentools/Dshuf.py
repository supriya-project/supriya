# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dshuf(DUGen):
    """
    A demand-rate random sequence generator.

    ::

        >>> sequence = (1, 2, 3)
        >>> dshuf = ugentools.Dshuf.new(
        ...     repeats=1,
        ...     sequence=sequence,
        ...     )
        >>> dshuf
        Dshuf()

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
        """
        Constructs a Dshuf.

        ::

            >>> sequence = (1, 2, 3)
            >>> dshuf = ugentools.Dshuf.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dshuf
            Dshuf()

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
        """
        Gets `repeats` input of Dshuf.

        ::

            >>> sequence = (1, 2, 3)
            >>> dshuf = ugentools.Dshuf.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dshuf.repeats
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('repeats')
        return self._inputs[index]

    @property
    def sequence(self):
        """
        Gets `sequence` input of Dshuf.

        ::

            >>> sequence = (1, 2, 3)
            >>> dshuf = ugentools.Dshuf.new(
            ...     repeats=1,
            ...     sequence=sequence,
            ...     )
            >>> dshuf.sequence
            (1.0, 2.0, 3.0)

        Returns ugen input.
        """
        index = self._ordered_input_names.index('sequence')
        return tuple(self._inputs[index:])
