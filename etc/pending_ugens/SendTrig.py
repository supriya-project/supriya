import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class SendTrig(UGen):
    """

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> send_trig = supriya.ugens.SendTrig.ar(
        ...     id=0,
        ...     source=source,
        ...     value=0,
        ...     )
        >>> send_trig
        SendTrig.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'source',
        'id',
        'value',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        id=0,
        source=None,
        value=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        id=0,
        source=None,
        value=0,
        ):
        """
        Constructs an audio-rate SendTrig.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> send_trig = supriya.ugens.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig
            SendTrig.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        id=0,
        source=None,
        value=0,
        ):
        """
        Constructs a control-rate SendTrig.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> send_trig = supriya.ugens.SendTrig.kr(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig
            SendTrig.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def id(self):
        """
        Gets `id` input of SendTrig.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> send_trig = supriya.ugens.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig.id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('id')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of SendTrig.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> send_trig = supriya.ugens.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def value(self):
        """
        Gets `value` input of SendTrig.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> send_trig = supriya.ugens.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig.value
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('value')
        return self._inputs[index]
