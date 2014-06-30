# -*- encoding: utf-8 -*-
import abc
import collections
from supriya.tools.ugentools.PseudoUGen import PseudoUGen


class SoundIn(PseudoUGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @staticmethod
    def ar(bus=0, **kwargs):
        from supriya.tools import ugentools
        channel_offset = ugentools.NumOutputBuses.ir()
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
        return ugentools.In.ar(
            bus=bus,
            channel_count=channel_count,
            )
