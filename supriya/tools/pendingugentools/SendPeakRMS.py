# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SendPeakRMS(UGen):
    r'''

    ::

        >>> send_peak_rms = ugentools.SendPeakRMS.(
        ...     cmd_name='/reply',
        ...     peak_lag=3,
        ...     reply_id=-1,
        ...     reply_rate=20,
        ...     sig=None,
        ...     )
        >>> send_peak_rms

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'sig',
        'reply_rate',
        'peak_lag',
        'cmd_name',
        'reply_id',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        cmd_name='/reply',
        peak_lag=3,
        reply_id=-1,
        reply_rate=20,
        sig=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            sig=sig,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        cmd_name='/reply',
        peak_lag=3,
        reply_id=-1,
        reply_rate=20,
        sig=None,
        ):
        r'''Constructs an audio-rate SendPeakRMS.

        ::

            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     cmd_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     sig=None,
            ...     )
            >>> send_peak_rms

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            sig=sig,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        cmd_name='/reply',
        peak_lag=3,
        reply_id=-1,
        reply_rate=20,
        sig=None,
        ):
        r'''Constructs a control-rate SendPeakRMS.

        ::

            >>> send_peak_rms = ugentools.SendPeakRMS.kr(
            ...     cmd_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     sig=None,
            ...     )
            >>> send_peak_rms

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            peak_lag=peak_lag,
            reply_id=reply_id,
            reply_rate=reply_rate,
            sig=sig,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def cmd_name(self):
        r'''Gets `cmd_name` input of SendPeakRMS.

        ::

            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     cmd_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     sig=None,
            ...     )
            >>> send_peak_rms.cmd_name

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('cmd_name')
        return self._inputs[index]

    @property
    def peak_lag(self):
        r'''Gets `peak_lag` input of SendPeakRMS.

        ::

            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     cmd_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     sig=None,
            ...     )
            >>> send_peak_rms.peak_lag

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('peak_lag')
        return self._inputs[index]

    @property
    def reply_id(self):
        r'''Gets `reply_id` input of SendPeakRMS.

        ::

            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     cmd_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     sig=None,
            ...     )
            >>> send_peak_rms.reply_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reply_id')
        return self._inputs[index]

    @property
    def reply_rate(self):
        r'''Gets `reply_rate` input of SendPeakRMS.

        ::

            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     cmd_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     sig=None,
            ...     )
            >>> send_peak_rms.reply_rate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reply_rate')
        return self._inputs[index]

    @property
    def sig(self):
        r'''Gets `sig` input of SendPeakRMS.

        ::

            >>> send_peak_rms = ugentools.SendPeakRMS.ar(
            ...     cmd_name='/reply',
            ...     peak_lag=3,
            ...     reply_id=-1,
            ...     reply_rate=20,
            ...     sig=None,
            ...     )
            >>> send_peak_rms.sig

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('sig')
        return self._inputs[index]