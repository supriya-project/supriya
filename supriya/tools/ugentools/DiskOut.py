# -*- encoding: utf-8 -*-
import collections
from supriya.tools.synthdeftools.UGen import UGen


class DiskOut(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Disk I/O UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen