import abc
import collections
from supriya.ugens.PseudoUGen import PseudoUGen


class SoundIn(PseudoUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Input/Output UGens'

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @staticmethod
    def ar(bus=0):
        import supriya.ugens
        channel_offset = supriya.ugens.NumOutputBuses.ir()
        if isinstance(bus, collections.Iterable):
            assert all(isinstance(x, int) for x in bus)
            bus = tuple(sorted(bus))
        else:
            assert isinstance(bus, int)
            bus = (bus,)
        if bus == tuple(range(min(bus), max(bus) + 1)):
            channel_count = len(bus)
            bus = min(bus)
        else:
            channel_count = 1
        bus = bus + channel_offset
        return supriya.ugens.In.ar(
            bus=bus,
            channel_count=channel_count,
            )
