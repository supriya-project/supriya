# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class RecordBuf(UGen):

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
        done_action=0,
        input_array=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            done_action=done_action,
            input_array=input_array,
            loop=loop,
            offset=offset,
            pre_level=pre_level,
            rec_level=rec_level,
            run=run,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bufnum=0,
        done_action=0,
        input_array=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            done_action=done_action,
            input_array=input_array,
            loop=loop,
            offset=offset,
            pre_level=pre_level,
            rec_level=rec_level,
            run=run,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bufnum=0,
        done_action=0,
        input_array=None,
        loop=1,
        offset=0,
        pre_level=0,
        rec_level=1,
        run=1,
        trigger=1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bufnum=bufnum,
            done_action=done_action,
            input_array=input_array,
            loop=loop,
            offset=offset,
            pre_level=pre_level,
            rec_level=rec_level,
            run=run,
            trigger=trigger,
            )
        return ugen
