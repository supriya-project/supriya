import collections
from supriya.synthdefs.UGen import UGen
from supriya.synthdefs import ArgumentSpecification


class Out(UGen):

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    @classmethod
    def _new(cls, calculation_rate, special_index, bus=0, channels=None):
        ugen = cls(
            calculation_rate=calculation_rate,
            special_index=special_index,
            )
        ArgumentSpecification('bus').configure(ugen, bus)
        if not isinstance(channels, collections.Sequence):
            channels = [channels]
        for channel in channels:
            ArgumentSpecification('source').configure(ugen, channel)
        return ugen
