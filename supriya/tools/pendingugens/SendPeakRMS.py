# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SendPeakRMS(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
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
        from supriya.tools import synthdeftools
        calculation_rate = None
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
        from supriya.tools import synthdeftools
        calculation_rate = None
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
