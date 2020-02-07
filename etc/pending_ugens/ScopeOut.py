import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import UGen


class ScopeOut(UGen):
    """

    ::

        >>> scope_out = supriya.ugens.ScopeOut.ar(
        ...     buffer_id=0,
        ...     input_array=input_array,
        ...     )
        >>> scope_out
        ScopeOut.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'input_array',
        'buffer_id',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=0,
        input_array=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=0,
        input_array=None,
        ):
        """
        Constructs an audio-rate ScopeOut.

        ::

            >>> scope_out = supriya.ugens.ScopeOut.ar(
            ...     buffer_id=0,
            ...     input_array=input_array,
            ...     )
            >>> scope_out
            ScopeOut.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=0,
        input_array=None,
        ):
        """
        Constructs a control-rate ScopeOut.

        ::

            >>> scope_out = supriya.ugens.ScopeOut.kr(
            ...     buffer_id=0,
            ...     input_array=input_array,
            ...     )
            >>> scope_out
            ScopeOut.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input_array=input_array,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of ScopeOut.

        ::

            >>> scope_out = supriya.ugens.ScopeOut.ar(
            ...     buffer_id=0,
            ...     input_array=input_array,
            ...     )
            >>> scope_out.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def input_array(self):
        """
        Gets `input_array` input of ScopeOut.

        ::

            >>> scope_out = supriya.ugens.ScopeOut.ar(
            ...     buffer_id=0,
            ...     input_array=input_array,
            ...     )
            >>> scope_out.input_array

        Returns ugen input.
        """
        index = self._ordered_input_names.index('input_array')
        return self._inputs[index]
