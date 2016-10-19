# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class DemandEnvGen(UGen):
    r"""

    ::

        >>> demand_env_gen = ugentools.DemandEnvGen.ar(
        ...     curve=0,
        ...     done_action=0,
        ...     duration=duration,
        ...     gate=1,
        ...     level=level,
        ...     level_bias=0,
        ...     level_scale=1,
        ...     reset=1,
        ...     shape=1,
        ...     time_scale=1,
        ...     )
        >>> demand_env_gen
        DemandEnvGen.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'level',
        'duration',
        'shape',
        'curve',
        'gate',
        'reset',
        'level_scale',
        'level_bias',
        'time_scale',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        curve=0,
        done_action=0,
        duration=None,
        gate=1,
        level=None,
        level_bias=0,
        level_scale=1,
        reset=1,
        shape=1,
        time_scale=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            curve=curve,
            done_action=done_action,
            duration=duration,
            gate=gate,
            level=level,
            level_bias=level_bias,
            level_scale=level_scale,
            reset=reset,
            shape=shape,
            time_scale=time_scale,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        curve=0,
        done_action=0,
        duration=None,
        gate=1,
        level=None,
        level_bias=0,
        level_scale=1,
        reset=1,
        shape=1,
        time_scale=1,
        ):
        r"""
        Constructs an audio-rate DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen
            DemandEnvGen.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curve=curve,
            done_action=done_action,
            duration=duration,
            gate=gate,
            level=level,
            level_bias=level_bias,
            level_scale=level_scale,
            reset=reset,
            shape=shape,
            time_scale=time_scale,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        curve=0,
        done_action=0,
        duration=None,
        gate=1,
        level=None,
        level_bias=0,
        level_scale=1,
        reset=1,
        shape=1,
        time_scale=1,
        ):
        r"""
        Constructs a control-rate DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.kr(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen
            DemandEnvGen.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            curve=curve,
            done_action=done_action,
            duration=duration,
            gate=gate,
            level=level,
            level_bias=level_bias,
            level_scale=level_scale,
            reset=reset,
            shape=shape,
            time_scale=time_scale,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def curve(self):
        r"""
        Gets `curve` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.curve
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('curve')
        return self._inputs[index]

    @property
    def done_action(self):
        r"""
        Gets `done_action` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.done_action
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def duration(self):
        r"""
        Gets `duration` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.duration

        Returns ugen input.
        """
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def gate(self):
        r"""
        Gets `gate` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.gate
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('gate')
        return self._inputs[index]

    @property
    def level(self):
        r"""
        Gets `level` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.level

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def level_bias(self):
        r"""
        Gets `level_bias` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.level_bias
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level_bias')
        return self._inputs[index]

    @property
    def level_scale(self):
        r"""
        Gets `level_scale` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.level_scale
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level_scale')
        return self._inputs[index]

    @property
    def reset(self):
        r"""
        Gets `reset` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.reset
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def shape(self):
        r"""
        Gets `shape` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.shape
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('shape')
        return self._inputs[index]

    @property
    def time_scale(self):
        r"""
        Gets `time_scale` input of DemandEnvGen.

        ::

            >>> demand_env_gen = ugentools.DemandEnvGen.ar(
            ...     curve=0,
            ...     done_action=0,
            ...     duration=duration,
            ...     gate=1,
            ...     level=level,
            ...     level_bias=0,
            ...     level_scale=1,
            ...     reset=1,
            ...     shape=1,
            ...     time_scale=1,
            ...     )
            >>> demand_env_gen.time_scale
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('time_scale')
        return self._inputs[index]
