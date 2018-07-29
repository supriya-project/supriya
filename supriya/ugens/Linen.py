from supriya.ugens.UGen import UGen


class Linen(UGen):
    """
    A simple line generating unit generator.

    ::

        >>> supriya.ugens.Linen.kr()
        Linen.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'gate',
        'attack_time',
        'sustain_level',
        'release_time',
        'done_action',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attack_time=0.01,
        done_action=0,
        gate=1.,
        calculation_rate=None,
        release_time=1.,
        sustain_level=1.,
        ):
        UGen.__init__(
            self,
            attack_time=attack_time,
            done_action=done_action,
            gate=gate,
            calculation_rate=calculation_rate,
            release_time=release_time,
            sustain_level=sustain_level,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        attack_time=0.01,
        done_action=0,
        gate=1.,
        calculation_rate=None,
        release_time=1.,
        sustain_level=1.,
        ):
        """
        Constructs an audio-rate line generator.

        ::

            >>> supriya.ugens.Linen.kr(
            ...     attack_time=5.5,
            ...     done_action=supriya.synthdefs.DoneAction.FREE_SYNTH,
            ...     release_time=0.5,
            ...     sustain_level=0.1,
            ...     )
            Linen.kr()

        Returns unit generator graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            attack_time=attack_time,
            done_action=done_action,
            gate=gate,
            calculation_rate=calculation_rate,
            release_time=release_time,
            sustain_level=sustain_level,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def attack_time(self):
        """
        Gets `attack_time` input of Linen.

        ::

            >>> attack_time = 0.01
            >>> linen = supriya.ugens.Linen.kr(
            ...     attack_time=attack_time,
            ...     )
            >>> linen.attack_time
            0.01

        Returns input.
        """
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def done_action(self):
        """
        Gets `done_action` input of Linen.

        ::

            >>> done_action = 0
            >>> linen = supriya.ugens.Linen.kr(
            ...     done_action=done_action,
            ...     )
            >>> linen.done_action
            0.0

        Returns input.
        """
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def gate(self):
        """
        Gets `gate` input of Linen.

        ::

            >>> gate = 1
            >>> linen = supriya.ugens.Linen.kr(
            ...     gate=gate,
            ...     )
            >>> linen.gate
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('gate')
        return self._inputs[index]

    @property
    def has_done_flag(self):
        """
        Is true if UGen has a done flag.

        Returns boolean.
        """
        return True

    @property
    def release_time(self):
        """
        Gets `release_time` input of Linen.

        ::

            >>> release_time = 1
            >>> linen = supriya.ugens.Linen.kr(
            ...     release_time=release_time,
            ...     )
            >>> linen.release_time
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('release_time')
        return self._inputs[index]

    @property
    def sustain_level(self):
        """
        Gets `sustain_level` input of Linen.

        ::

            >>> sustain_level = 1
            >>> linen = supriya.ugens.Linen.kr(
            ...     sustain_level=sustain_level,
            ...     )
            >>> linen.sustain_level
            1.0

        Returns input.
        """
        index = self._ordered_input_names.index('sustain_level')
        return self._inputs[index]
