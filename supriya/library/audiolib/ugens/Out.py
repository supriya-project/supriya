import collections
from supriya.library.audiolib import Argument
from supriya.library.audiolib.UGen import UGen


class Out(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        bus=0,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            special_index=special_index,
            )
        Argument('bus').configure(self, bus)
        if not isinstance(source, collections.Sequence):
            source = [source]
        for single_source in source:
            Argument('source').configure(self, single_source)

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, **kwargs):
        
        ugen = cls(
            calculation_rate=UGen.Rate.AUDIO_RATE,
            special_index=0,
            bus=kwargs.get('bus'),
            source=kwargs.get('source'),
            )
        return ugen

    @classmethod
    def kr(cls, **kwargs):
        ugen = cls(
            calculation_rate=UGen.Rate.CONTROL_RATE,
            special_index=0,
            bus=kwargs.get('bus'),
            source=kwargs.get('source'),
            )
        return ugen

