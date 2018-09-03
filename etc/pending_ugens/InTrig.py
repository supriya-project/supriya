import collections
from supriya.enums import CalculationRate
from supriya.ugens.AbstractIn import AbstractIn


class InTrig(AbstractIn):
    """

    ::

        >>> in_trig = supriya.ugens.InTrig.ar(
        ...     bus=0,
        ...     channel_count=1,
        ...     )
        >>> in_trig
        InTrig.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'bus',
        'channel_count',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        channel_count=1,
        ):
        AbstractIn.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    # def isInputUGen(): ...

    @classmethod
    def kr(
        cls,
        bus=0,
        channel_count=1,
        ):
        """
        Constructs a control-rate InTrig.

        ::

            >>> in_trig = supriya.ugens.InTrig.kr(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig
            InTrig.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of InTrig.

        ::

            >>> in_trig = supriya.ugens.InTrig.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig.bus
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of InTrig.

        ::

            >>> in_trig = supriya.ugens.InTrig.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]
