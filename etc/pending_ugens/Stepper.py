import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class Stepper(UGen):
    """

    ::

        >>> stepper = supriya.ugens.Stepper.ar(
        ...     maximum=7,
        ...     minimum=0,
        ...     reset=0,
        ...     resetval=resetval,
        ...     step=1,
        ...     trigger=0,
        ...     )
        >>> stepper
        Stepper.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'trigger',
        'reset',
        'minimum',
        'maximum',
        'step',
        'resetval',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        maximum=7,
        minimum=0,
        reset=0,
        resetval=None,
        step=1,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            reset=reset,
            resetval=resetval,
            step=step,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        maximum=7,
        minimum=0,
        reset=0,
        resetval=None,
        step=1,
        trigger=0,
        ):
        """
        Constructs an audio-rate Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.ar(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper
            Stepper.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            reset=reset,
            resetval=resetval,
            step=step,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        maximum=7,
        minimum=0,
        reset=0,
        resetval=None,
        step=1,
        trigger=0,
        ):
        """
        Constructs a control-rate Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.kr(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper
            Stepper.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            reset=reset,
            resetval=resetval,
            step=step,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        """
        Gets `maximum` input of Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.ar(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper.maximum
            7.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.ar(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper.minimum
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def reset(self):
        """
        Gets `reset` input of Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.ar(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper.reset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def resetval(self):
        """
        Gets `resetval` input of Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.ar(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper.resetval

        Returns ugen input.
        """
        index = self._ordered_input_names.index('resetval')
        return self._inputs[index]

    @property
    def step(self):
        """
        Gets `step` input of Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.ar(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper.step
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('step')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Stepper.

        ::

            >>> stepper = supriya.ugens.Stepper.ar(
            ...     maximum=7,
            ...     minimum=0,
            ...     reset=0,
            ...     resetval=resetval,
            ...     step=1,
            ...     trigger=0,
            ...     )
            >>> stepper.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
