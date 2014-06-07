# -*- encoding: utf-8 -*-
from supriya.library.controllib.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy):
    r'''A bus.

    ::

        >>> from supriya import audiolib
        >>> from supriya import controllib
        >>> bus = controllib.Bus(
        ...    calculation_rate=audiolib.UGen.Rate.AUDIO_RATE,
        ...    channel_count=1,
        ...    )

    '''
    ### CLASS VARIABLES ###

    __slots__ = (
        '_bus_index',
        '_calculation_rate',
        '_channel_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        channel_count=1,
        ):
        from supriya.library import audiolib
        ServerObjectProxy.__init__(self)
        if calculation_rate is None:
            calculation_rate = audiolib.UGen.Rate.AUDIO_RATE
        assert isinstance(calculation_rate, audiolib.UGen.Rate), \
            calculation_rate
        assert 0 < calculation_rate
        self._calculation_rate = calculation_rate
        self._channel_count = int(channel_count)
        self._bus_index = None

    ### PUBLIC METHODS ###

    def allocate(self, server_session=None):
        ServerObjectProxy.allocate(self)
        self._bus_index = server_session.audio_bus_allocator.allocate(
            self.channel_count,
            )

    def ar(self):
        from supriya.library import audiolib
        if self.calculation_rate == audiolib.UGen.Rate.AUDIO_RATE:
            result = audiolib.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = audiolib.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = audiolib.K2A.ar(
                source=result,
                )
        return result

    @classmethod
    def audio(
        cls,
        channel_count=1,
        server=None,
        ):
        from supriya.library import audiolib
        from supriya.library import controllib
        server = server or controllib.Server()
        bus_index = server.audio_bus_allocator.allocate(channel_count)
        if bus_index is None:
            raise Exception
        bus = cls(
            bus_index=bus_index,
            calculation_rate=audiolib.UGen.Rate.AUDIO_RATE,
            channel_count=channel_count,
            server=server,
            )
        return bus

    @classmethod
    def control(
        cls,
        channel_count=1,
        server=None,
        ):
        from supriya.library import audiolib
        from supriya.library import controllib
        server = server or controllib.Server()
        bus_index = server.control_bus_allocator.allocate(channel_count)
        if bus_index is None:
            raise Exception
        bus = cls(
            bus_index=bus_index,
            calculation_rate=audiolib.UGen.Rate.AUDIO_RATE,
            channel_count=channel_count,
            server=server,
            )
        return bus

    def free(self):
        from supriya.library import audiolib
        ServerObjectProxy.free(self)
        assert self.bus_index is not None
        if self.calculation_rate == audiolib.UGen.Rate.AUDIO_RATE:
            self.server.audio_bus_allocator.free(self.bus_index)
        else:
            self.server.control_bus_allocator.free(self.bus_index)
        self._bus_index = None

    def kr(self):
        from supriya.library import audiolib
        if self.calculation_rate == audiolib.UGen.Rate.CONTROL_RATE:
            result = audiolib.In.kr(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
        else:
            result = audiolib.In.ar(
                bus=self.bus_index,
                channel_count=self.channel_count,
                )
            result = audiolib.A2K.ar(
                source=result,
                )
        return result

    def make_set_message(self, *args):
        assert self.is_settable
        assert len(args) <= self.channel_count
        message = ('/c_set',)
        for index, value in enumerate(args):
            index += self.bus_index
            message += (index, value)
        return message
        self.server.send_message(message)

    def set(self, *args):
        message = self.make_set_message(*args)
        self.server.send_message(message)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_index(self):
        return self._bus_index

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def channel_count(self):
        return self._channel_count

    @property
    def is_settable(self):
        from supriya.library import audiolib
        return self.calculation_rate != audiolib.UGen.Rate.AUDIO_RATE

    @property
    def map_symbol(self):
        from supriya.library import audiolib
        assert self.bus_index is not None
        if self.calculation_rate == audiolib.UGen.Rate.AUDIO_RATE:
            string = 'a{}'
        else:
            string = 'c{}'
        string = string.format(self.bus_index)
        return string
