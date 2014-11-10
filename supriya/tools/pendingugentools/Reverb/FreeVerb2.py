# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class FreeVerb2(MultiOutUGen):

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
        damp=0.5,
        in_2=None,
        mix=0.33,
        room=0.5,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damp=damp,
            in_2=in_2,
            mix=mix,
            room=room,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damp=0.5,
        in_2=None,
        mix=0.33,
        room=0.5,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damp=damp,
            in_2=in_2,
            mix=mix,
            room=room,
            source=source,
            )
        return ugen
