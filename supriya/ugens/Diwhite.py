from supriya.ugens.Dwhite import Dwhite


class Diwhite(Dwhite):
    """
    An integer demand-rate white noise random generator.

    ::

        >>> diwhite = supriya.ugens.Diwhite(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     )
        >>> diwhite
        Diwhite()

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
        Dwhite.__init__(
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
        Constructs a Diwhite.

        ::

            >>> diwhite = supriya.ugens.Diwhite.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite
            Diwhite()

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
        Gets `length` input of Diwhite.

        ::

            >>> diwhite = supriya.ugens.Diwhite(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.length
            inf

        Returns ugen input.
        """
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def maximum(self):
        """
        Gets `maximum` input of Diwhite.

        ::

            >>> diwhite = supriya.ugens.Diwhite(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of Diwhite.

        ::

            >>> diwhite = supriya.ugens.Diwhite(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     )
            >>> diwhite.minimum
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]
