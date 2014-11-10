# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PlayBuf(MultiOutUGen):

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
        bufnum=0,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_pos=0,
        trigger=1,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_pos=start_pos,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufnum=0,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_pos=0,
        trigger=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_pos=start_pos,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bufnum=0,
        channel_count=None,
        done_action=0,
        loop=0,
        rate=1,
        start_pos=0,
        trigger=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            channel_count=channel_count,
            done_action=done_action,
            loop=loop,
            rate=rate,
            start_pos=start_pos,
            trigger=trigger,
            )
        return ugen
