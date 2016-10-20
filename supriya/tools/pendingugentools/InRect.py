# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class InRect(UGen):
    """

    ::

        >>> in_rect = ugentools.InRect.ar(
        ...     rect=rect,
        ...     x=0,
        ...     y=0,
        ...     )
        >>> in_rect
        InRect.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'x',
        'y',
        'rect',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        rect=None,
        x=0,
        y=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            rect=rect,
            x=x,
            y=y,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        rect=None,
        x=0,
        y=0,
        ):
        """
        Constructs an audio-rate InRect.

        ::

            >>> in_rect = ugentools.InRect.ar(
            ...     rect=rect,
            ...     x=0,
            ...     y=0,
            ...     )
            >>> in_rect
            InRect.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rect=rect,
            x=x,
            y=y,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        rect=None,
        x=0,
        y=0,
        ):
        """
        Constructs a control-rate InRect.

        ::

            >>> in_rect = ugentools.InRect.kr(
            ...     rect=rect,
            ...     x=0,
            ...     y=0,
            ...     )
            >>> in_rect
            InRect.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rect=rect,
            x=x,
            y=y,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def rect(self):
        """
        Gets `rect` input of InRect.

        ::

            >>> in_rect = ugentools.InRect.ar(
            ...     rect=rect,
            ...     x=0,
            ...     y=0,
            ...     )
            >>> in_rect.rect

        Returns ugen input.
        """
        index = self._ordered_input_names.index('rect')
        return self._inputs[index]

    @property
    def x(self):
        """
        Gets `x` input of InRect.

        ::

            >>> in_rect = ugentools.InRect.ar(
            ...     rect=rect,
            ...     x=0,
            ...     y=0,
            ...     )
            >>> in_rect.x
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('x')
        return self._inputs[index]

    @property
    def y(self):
        """
        Gets `y` input of InRect.

        ::

            >>> in_rect = ugentools.InRect.ar(
            ...     rect=rect,
            ...     x=0,
            ...     y=0,
            ...     )
            >>> in_rect.y
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('y')
        return self._inputs[index]
