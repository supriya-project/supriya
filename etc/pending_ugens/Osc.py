import collections
from supriya.enums import CalculationRate
from supriya.synthdefs import PureUGen


class Osc(PureUGen):
    """

    ::

        >>> osc = supriya.ugens.Osc.ar(
        ...     buffer_id=buffer_id,
        ...     frequency=440,
        ...     phase=0,
        ...     )
        >>> osc
        Osc.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'buffer_id',
        'frequency',
        'phase',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        """
        Constructs an audio-rate Osc.

        ::

            >>> osc = supriya.ugens.Osc.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc
            Osc.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        frequency=440,
        phase=0,
        ):
        """
        Constructs a control-rate Osc.

        ::

            >>> osc = supriya.ugens.Osc.kr(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc
            Osc.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            frequency=frequency,
            phase=phase,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of Osc.

        ::

            >>> osc = supriya.ugens.Osc.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc.buffer_id

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of Osc.

        ::

            >>> osc = supriya.ugens.Osc.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def phase(self):
        """
        Gets `phase` input of Osc.

        ::

            >>> osc = supriya.ugens.Osc.ar(
            ...     buffer_id=buffer_id,
            ...     frequency=440,
            ...     phase=0,
            ...     )
            >>> osc.phase
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('phase')
        return self._inputs[index]
