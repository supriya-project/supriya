# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dbufrd(DUGen):
    r"""
    A buffer-reading demand-rate UGen.

    ::

        >>> dbufrd = ugentools.Dbufrd(
        ...     buffer_id=0,
        ...     loop=1,
        ...     phase=0,
        ...     )
        >>> dbufrd
        Dbufrd()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'phase',
        'loop',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        buffer_id=0,
        loop=1,
        phase=0,
        ):
        DUGen.__init__(
            self,
            buffer_id=buffer_id,
            loop=loop,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=0,
        loop=1,
        phase=0,
        ):
        r"""
        Constructs a Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd.new(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd
            Dbufrd()

        Returns ugen graph.
        """
        ugen = cls._new_expanded(
            buffer_id=buffer_id,
            loop=loop,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r"""
        Gets `buffer_id` input of Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        r"""
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True

    @property
    def loop(self):
        r"""
        Gets `loop` input of Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd.loop
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('loop')
        return self._inputs[index]

    @property
    def phase(self):
        r"""
        Gets `phase` input of Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd.phase
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]
