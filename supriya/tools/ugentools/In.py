# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class In(MultiOutUGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _argument_specifications = (
        Argument('bus', 0),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus=0,
        calculation_rate=None,
        channel_count=1,
        ):
        MultiOutUGen.__init__(
            self,
            bus=bus,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            )
