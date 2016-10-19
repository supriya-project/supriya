# -*- encoding: utf-8 -*-
import collections
from supriya.tools.ugentools.UGen import UGen


class SendPeakRMS(UGen):
    r"""
    Tracks peak and power of a signal for GUI applications.

    ::

        >>> source = ugentools.In.ar(channel_count=4)
        >>> send_peak_rms = ugentools.SendPeakRMS.kr(
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

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'reply_rate',
        'peak_lag',
        'reply_id',
        )

    _unexpanded_argument_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        command_name='/reply',
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
        self._configure_input('source', len(source))
        for input_ in source:
            self._configure_input('source', input_)
        self._configure_input('command_name', len(command_name))
        for character in command_name:
            self._configure_input('label', ord(character))

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        command_name='/reply',
        peak_lag=3,
        reply_id=-1,
        reply_rate=20,
        source=None,
        ):
        r"""
        Constructs an audio-rate SendPeakRMS.

        ::

            >>> source = ugentools.In.ar(channel_count=4)
            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
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
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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
        cls,
        command_name='/reply',
        peak_lag=3,
        reply_id=-1,
        reply_rate=20,
        source=None,
        ):
        r"""
        Constructs a control-rate SendPeakRMS.

        ::

            >>> source = ugentools.In.ar(channel_count=4)
            >>> send_peak_rms = ugentools.SendPeakRMS.kr(
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
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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
        r"""
        Gets `command_name` input of SendPeakRMS.

        ::

            >>> source = ugentools.In.ar(channel_count=4)
            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
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
        index = self._ordered_input_names.index('reply_id') + 1
        source_length = int(self._inputs[index])
        index += source_length + 2
        characters = self._inputs[index:]
        characters = [chr(int(_)) for _ in characters]
        command_name = ''.join(characters)
        return command_name

    @property
    def peak_lag(self):
        r"""
        Gets `peak_lag` input of SendPeakRMS.

        ::

            >>> source = ugentools.In.ar(channel_count=4)
            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms.peak_lag
            3.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('peak_lag')
        return self._inputs[index]

    @property
    def reply_id(self):
        r"""
        Gets `reply_id` input of SendPeakRMS.

        ::

            >>> source = ugentools.In.ar(channel_count=4)
            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms.reply_id
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reply_id')
        return self._inputs[index]

    @property
    def reply_rate(self):
        r"""
        Gets `reply_rate` input of SendPeakRMS.

        ::

            >>> source = ugentools.In.ar(channel_count=4)
            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms.reply_rate
            20.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reply_rate')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of SendPeakRMS.

        ::

            >>> source = ugentools.In.ar(channel_count=4)
            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     command_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     source=source,
            ...     )
            >>> send_peak_rms.source
            (OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=4
                    ),
                output_index=0
                ), OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=4
                    ),
                output_index=1
                ), OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=4
                    ),
                output_index=2
                ), OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=4
                    ),
                output_index=3
                ))

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reply_id') + 1
        source_length = int(self._inputs[index])
        start = index + 1
        stop = start + source_length
        return tuple(self._inputs[start:stop])
