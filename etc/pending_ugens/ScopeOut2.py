from supriya.ugens.UGen import UGen


class ScopeOut2(UGen):
    """

    ::

        >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
        ...     input_array=input_array,
        ...     max_frames=4096,
        ...     scope_frames=scope_frames,
        ...     scope_num=0,
        ...     )
        >>> scope_out_2
        ScopeOut2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'input_array',
        'scope_num',
        'max_frames',
        'scope_frames',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        input_array=None,
        max_frames=4096,
        scope_frames=None,
        scope_num=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            input_array=input_array,
            max_frames=max_frames,
            scope_frames=scope_frames,
            scope_num=scope_num,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        input_array=None,
        max_frames=4096,
        scope_frames=None,
        scope_num=0,
        ):
        """
        Constructs an audio-rate ScopeOut2.

        ::

            >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
            ...     input_array=input_array,
            ...     max_frames=4096,
            ...     scope_frames=scope_frames,
            ...     scope_num=0,
            ...     )
            >>> scope_out_2
            ScopeOut2.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input_array=input_array,
            max_frames=max_frames,
            scope_frames=scope_frames,
            scope_num=scope_num,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        input_array=None,
        max_frames=4096,
        scope_frames=None,
        scope_num=0,
        ):
        """
        Constructs a control-rate ScopeOut2.

        ::

            >>> scope_out_2 = supriya.ugens.ScopeOut2.kr(
            ...     input_array=input_array,
            ...     max_frames=4096,
            ...     scope_frames=scope_frames,
            ...     scope_num=0,
            ...     )
            >>> scope_out_2
            ScopeOut2.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input_array=input_array,
            max_frames=max_frames,
            scope_frames=scope_frames,
            scope_num=scope_num,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def input_array(self):
        """
        Gets `input_array` input of ScopeOut2.

        ::

            >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
            ...     input_array=input_array,
            ...     max_frames=4096,
            ...     scope_frames=scope_frames,
            ...     scope_num=0,
            ...     )
            >>> scope_out_2.input_array

        Returns ugen input.
        """
        index = self._ordered_input_names.index('input_array')
        return self._inputs[index]

    @property
    def max_frames(self):
        """
        Gets `max_frames` input of ScopeOut2.

        ::

            >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
            ...     input_array=input_array,
            ...     max_frames=4096,
            ...     scope_frames=scope_frames,
            ...     scope_num=0,
            ...     )
            >>> scope_out_2.max_frames
            4096.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('max_frames')
        return self._inputs[index]

    @property
    def scope_frames(self):
        """
        Gets `scope_frames` input of ScopeOut2.

        ::

            >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
            ...     input_array=input_array,
            ...     max_frames=4096,
            ...     scope_frames=scope_frames,
            ...     scope_num=0,
            ...     )
            >>> scope_out_2.scope_frames

        Returns ugen input.
        """
        index = self._ordered_input_names.index('scope_frames')
        return self._inputs[index]

    @property
    def scope_num(self):
        """
        Gets `scope_num` input of ScopeOut2.

        ::

            >>> scope_out_2 = supriya.ugens.ScopeOut2.ar(
            ...     input_array=input_array,
            ...     max_frames=4096,
            ...     scope_frames=scope_frames,
            ...     scope_num=0,
            ...     )
            >>> scope_out_2.scope_num
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('scope_num')
        return self._inputs[index]
