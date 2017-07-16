import collections
from supriya.tools.ugentools.UGen import UGen


class LocalOut(UGen):
    """
    A SynthDef-local bus output.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> ugentools.LocalOut.ar(
        ...     source=source,
        ...     )
        LocalOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        """
        Constructs an audio-rate SynthDef-local bus output.

        ::

            >>> source = ugentools.SinOsc.ar(
            ...     frequency=[440, 442],
            ...     )
            >>> local_out = ugentools.LocalOut.ar(
            ...     source=source,
            ...     )
            >>> local_out
            LocalOut.ar()
        
        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate SynthDef-local bus output.

        ::

            >>> source = ugentools.SinOsc.kr(
            ...     frequency=[4, 2],
            ...     )
            >>> local_out = ugentools.LocalOut.kr(
            ...     source=source,
            ...     )
            >>> local_out
            LocalOut.kr()
        
        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of local_out.

        ::

            >>> source = ugentools.WhiteNoise.ar()
            >>> local_out = ugentools.LocalOut.ar(
            ...     source=source,
            ...     )
            >>> local_out.source
            (OutputProxy(
                source=WhiteNoise(
                    calculation_rate=CalculationRate.AUDIO
                    ),
                output_index=0
                ),)

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return tuple(self._inputs[index:])
