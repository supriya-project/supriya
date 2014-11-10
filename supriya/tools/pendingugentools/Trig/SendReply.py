# -*- encoding: utf-8 -*-
from supriya.tools.pendingugentools.SendTrig import SendTrig


class SendReply(SendTrig):

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
        reply_id=-1,
        trigger=0,
        values=None,
        ):
        SendTrig.__init__(
            self,
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            reply_id=reply_id,
            trigger=trigger,
            values=values,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        cmd_name='/reply',
        reply_id=-1,
        trigger=0,
        values=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            reply_id=reply_id,
            trigger=trigger,
            values=values,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        cmd_name='/reply',
        reply_id=-1,
        trigger=0,
        values=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            reply_id=reply_id,
            trigger=trigger,
            values=values,
            )
        return ugen

    # def new1(): ...
