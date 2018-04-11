from supriya.ugens.DUGen import DUGen


class Dbrown(DUGen):
    """
    A demand-rate brownian movement generator.

    ::

        >>> dbrown = supriya.ugens.Dbrown.new(
        ...     length=float('inf'),
        ...     maximum=1,
        ...     minimum=0,
        ...     step=0.01,
        ...     )
        >>> dbrown
        Dbrown()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'step',
        'length',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        length=float('inf'),
        maximum=1,
        minimum=0,
        step=0.01,
        ):
        if length is None:
            length = float('inf')
        DUGen.__init__(
            self,
            length=length,
            maximum=maximum,
            minimum=minimum,
            step=step,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        length=float('inf'),
        maximum=1,
        minimum=0,
        step=0.01,
        ):
        """
        Constructs a Dbrown.

        ::

            >>> dbrown = supriya.ugens.Dbrown.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     step=0.01,
            ...     )
            >>> dbrown
            Dbrown()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            length=length,
            maximum=maximum,
            minimum=minimum,
            step=step,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        """
        Gets `length` input of Dbrown.

        ::

            >>> dbrown = supriya.ugens.Dbrown.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.length
            inf

        Returns ugen input.
        """
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def maximum(self):
        """
        Gets `maximum` input of Dbrown.

        ::

            >>> dbrown = supriya.ugens.Dbrown.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of Dbrown.

        ::

            >>> dbrown = supriya.ugens.Dbrown.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.minimum
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def step(self):
        """
        Gets `step` input of Dbrown.

        ::

            >>> dbrown = supriya.ugens.Dbrown.new(
            ...     length=float('inf'),
            ...     maximum=1,
            ...     minimum=0,
            ...     step=0.01,
            ...     )
            >>> dbrown.step
            0.01

        Returns ugen input.
        """
        index = self._ordered_input_names.index('step')
        return self._inputs[index]
