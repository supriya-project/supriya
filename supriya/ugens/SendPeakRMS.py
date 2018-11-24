import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class SendPeakRMS(UGen):
    """
    Tracks peak and power of a signal for GUI applications.

    ::

        >>> source = supriya.ugens.In.ar(channel_count=4)
        >>> send_peak_rms = supriya.ugens.SendPeakRMS.kr(
        ...     command_name='/reply',
        ...     peak_lag=3,
        ...     reply_id=-1,
        ...     reply_rate=20,
        ...     source=source,
        ...     )
        >>> send_peak_rms
        SendPeakRMS.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Utility UGens"

    _default_channel_count = 0

    _ordered_input_names = collections.OrderedDict(
        [("reply_rate", 20), ("peak_lag", 3), ("reply_id", -1)]
    )

    _unexpanded_argument_names = ("source",)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        command_name="/reply",
        peak_lag=3,
        reply_id=-1,
        reply_rate=20,
        source=None,
    ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
        )
        command_name = str(command_name)
        if not isinstance(source, collections.Sequence):
            source = (source,)
        self._configure_input("source", len(source))
        for input_ in source:
            self._configure_input("source", input_)
        self._configure_input("command_name", len(command_name))
        for character in command_name:
            self._configure_input("label", ord(character))

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls, command_name="/reply", peak_lag=3, reply_id=-1, reply_rate=20, source=None
    ):
        """
        Constructs an audio-rate SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.ar(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms
            SendPeakRMS.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_single(
            calculation_rate=calculation_rate,
            command_name=command_name,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            source=source,
        )
        return ugen

    @classmethod
    def kr(
        cls, command_name="/reply", peak_lag=3, reply_id=-1, reply_rate=20, source=None
    ):
        """
        Constructs a control-rate SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.kr(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms
            SendPeakRMS.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_single(
            calculation_rate=calculation_rate,
            command_name=command_name,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            source=source,
        )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def command_name(self):
        """
        Gets `command_name` input of SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.ar(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms.command_name
            '/reply'

        Returns ugen input.
        """
        index = tuple(self._ordered_input_names).index("reply_id") + 1
        source_length = int(self._inputs[index])
        index += source_length + 2
        characters = self._inputs[index:]
        characters = [chr(int(_)) for _ in characters]
        command_name = "".join(characters)
        return command_name

    @property
    def source(self):
        """
        Gets `source` input of SendPeakRMS.

        ::

            >>> source = supriya.ugens.In.ar(channel_count=4)
            >>> send_peak_rms = supriya.ugens.SendPeakRMS.ar(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms.source
            (In.ar()[0], In.ar()[1], In.ar()[2], In.ar()[3])

        Returns ugen input.
        """
        index = tuple(self._ordered_input_names).index("reply_id") + 1
        source_length = int(self._inputs[index])
        start = index + 1
        stop = start + source_length
        return tuple(self._inputs[start:stop])
