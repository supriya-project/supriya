# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.synthdeftools.UGen import UGen


class Line(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('start', 0),
        Argument('stop', 1),
        Argument('duration', 1),
        Argument('done_action', 0),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0.,
        duration=1.,
        start=0.,
        stop=1.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            start=start,
            stop=stop,
            )
