# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dwhite(DUGen):
    """
    A demand-rate white noise random generator.

    ::

        >>> dwhite = ugentools.Dwhite.new(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     )
        >>> dwhite
        Dwhite()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'length',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        length=float('inf'),
        maximum=1,
        minimum=0,
        ):
        if length is None:
            length = float('inf')
        DUGen.__init__(
            self,
            length=length,
            maximum=maximum,
            minimum=minimum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        length=float('inf'),
        maximum=1,
        minimum=0,
        ):
        """
        Constructs a Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> dwhite
            Dwhite()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            length=length,
            maximum=maximum,
            minimum=minimum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        """
        Gets `length` input of Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> dwhite.length
            inf

        Returns ugen input.
        """
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def maximum(self):
        """
        Gets `maximum` input of Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> dwhite.maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of Dwhite.

        ::

            >>> dwhite = ugentools.Dwhite.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> dwhite.minimum
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]
