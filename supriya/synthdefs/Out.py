from supriya.synthdefs.UGen import UGen
from supriya.synthdefs import ArgumentSpecification


class Out(UGen):

    ### PRIVATE METHODS ###

    def _get_outputs(self):
        return []

    @classmethod
    def _new(cls, calculation_rate, special_index, bus=0, input_=None):
        ugen = cls(
            calculation_rate=calculation_rate,
            special_index=special_index,
            )
#        ArgSpec('bus').configure(spec, bus)
#        if not is_mc(channels):
#            channels = [channels]
#             Just the one!
#        for channel in channels:
#            ArgSpec('source').configure(spec, channel)
        return ugen
