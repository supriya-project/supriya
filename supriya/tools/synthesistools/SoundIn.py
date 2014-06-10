# -*- encoding: utf-8 -*-
import abc
import collections
from supriya.tools.synthesistools.MultiOutUGen import MultiOutUGen


class SoundIn(MultiOutUGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, bus=0, **kwargs):
        from supriya.tools import synthesistools
        channel_offset = synthesistools.NumOutputBuses.ir()
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
        return synthesistools.In.ar(
            bus=bus,
            channel_count=channel_count,
            )
