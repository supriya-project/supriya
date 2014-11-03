# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class ScopeOut2(UGen):

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
        input_array=None,
        max_frames=4096,
        scope_frames=None,
        scope_num=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            input_array=input_array,
            max_frames=max_frames,
            scope_frames=scope_frames,
            scope_num=scope_num,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        input_array=None,
        max_frames=4096,
        scope_frames=None,
        scope_num=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input_array=input_array,
            max_frames=max_frames,
            scope_frames=scope_frames,
            scope_num=scope_num,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        input_array=None,
        max_frames=4096,
        scope_frames=None,
        scope_num=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            input_array=input_array,
            max_frames=max_frames,
            scope_frames=scope_frames,
            scope_num=scope_num,
            )
        return ugen
