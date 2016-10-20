# -*- encoding: utf-8 -*-
import collections
from abjad.tools import sequencetools
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class LocalIn(MultiOutUGen):
    """
    A SynthDef-local bus input.

    ::

        >>> ugentools.LocalIn.ar(channel_count=2)
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'default',
        )

    _unexpanded_input_names = (
        'default',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=1,
        default=0,
        ):
        if not isinstance(default, collections.Sequence):
            default = (default,)
        default = [float(_) for _ in default]
        default = sequencetools.repeat_sequence_to_length(
            default,
            channel_count,
            )
        default = default[:channel_count]
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        channel_count=1,
        default=0,
        ):
        """
        Constructs an audio-rate local in.

        ::

            >>> ugentools.LocalIn.ar(
            ...     channel_count=2,
            ...     default=(0.5, 0.75),
            ...     )
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        channel_count=1,
        default=0,
        ):
        """
        Constructs a control-rate local in.

        ::

            >>> ugentools.LocalIn.kr(
            ...     channel_count=2,
            ...     default=(0.5, 0.75),
            ...     )
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            default=default,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def default(self):
        """
        Gets `default` input of LocalIn.

        ::

            >>> local_in = ugentools.LocalIn.ar(channel_count=2)
            >>> local_in[0].source.default
            (0.0, 0.0)

        Returns ugen input.
        """
        index = self._ordered_input_names.index('default')
        return tuple(self._inputs[index:])
