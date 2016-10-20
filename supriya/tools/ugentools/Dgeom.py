# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dgeom(DUGen):
    """
    A demand-rate geometric series generator.

    ::

        >>> dgeom = ugentools.Dgeom.new(
        ...     grow=2,
        ...     length=float('inf'),
        ...     start=1,
        ...     )
        >>> dgeom
        Dgeom()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'start',
        'grow',
        'length',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        grow=2,
        length=float('inf'),
        start=1,
        ):
        if length is None:
            length = float('inf')
        DUGen.__init__(
            self,
            grow=grow,
            length=length,
            start=start,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        grow=2,
        length=float('inf'),
        start=1,
        ):
        """
        Constructs a Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.new(
            ...     grow=2,
            ...     length=float('inf'),
            ...     start=1,
            ...     )
            >>> dgeom
            Dgeom()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        ugen = cls._new_expanded(
            grow=grow,
            length=length,
            start=start,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def grow(self):
        """
        Gets `grow` input of Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.new(
            ...     grow=2,
            ...     length=float('inf'),
            ...     start=1,
            ...     )
            >>> dgeom.grow
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('grow')
        return self._inputs[index]

    @property
    def length(self):
        """
        Gets `length` input of Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.new(
            ...     grow=2,
            ...     length=float('inf'),
            ...     start=1,
            ...     )
            >>> dgeom.length
            inf

        Returns ugen input.
        """
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def start(self):
        """
        Gets `start` input of Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.new(
            ...     grow=2,
            ...     length=float('inf'),
            ...     start=1,
            ...     )
            >>> dgeom.start
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('start')
        return self._inputs[index]
