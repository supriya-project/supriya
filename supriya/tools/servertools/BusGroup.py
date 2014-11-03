# -*- encoding: utf-8 -*-
import collections
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class BusGroup(ServerObjectProxy, collections.Sequence):
    r'''A bus group.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_bus_id',
        '_buses',
        '_calculation_rate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_count=1,
        bus_id=None,
        rate=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        rate = synthdeftools.CalculationRate.from_expr(
            rate)
        self._calculation_rate = rate
        bus_count = int(bus_count)
        assert 0 < bus_count
        self._buses = tuple(
            servertools.Bus(
                bus_group_or_index=self,
                rate=self.rate,
                )
            for _ in range(bus_count)
            )
        assert isinstance(bus_id, (type(None), int))
        self._bus_id = bus_id

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.bus_id)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._buses[item]
        elif isinstance(item, slice):
            indices = item.indices(len(self))
            bus_count = indices[1] - indices[0]
            bus_group = BusGroup(
                bus_count=bus_count,
                bus_id=self.bus_id,
                rate=self.rate,
                )
            return bus_group

    def __int__(self):
        return int(self.bus_id)

    def __len__(self):
        return len(self._buses)

    def __repr__(self):
        string = '<{}: {{{}}} @ {}>'.format(
            type(self).__name__,
            len(self),
            self.bus_id
            )
        return string

    def __str__(self):
        return self.map_symbol

    ### PUBLIC METHODS ###

    def allocate(
        self,
        server=None,
        sync=False,
        ):
        from supriya.tools import servertools
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(self, server=server)
        allocator = servertools.Bus._get_allocator(
            rate=self.rate,
            server=self.server,
            )
        bus_id = allocator.allocate(len(self))
        if bus_id is None:
            ServerObjectProxy.free(self)
            raise ValueError
        self._bus_id = bus_id
        if sync:
            self.server.sync()
        return self

    def ar(self):
        r'''Creates an audio-rate input ugen subgraph.

        ::

            >>> from supriya.tools import servertools
            >>> audio_bus_group = servertools.BusGroup(
            ...     bus_id=8,
            ...     bus_count=4,
            ...     rate='audio',
            ...     )
            >>> ugen = audio_bus_group.ar()
            >>> print(str(ugen))
            SynthDef 0af6b551a643cad01e9994845ff4ae40 {
                const_0:8.0 -> 0_In[0:bus]
            }

        ::

            >>> control_bus_group = servertools.BusGroup(
            ...     bus_id=8,
            ...     bus_count=4,
            ...     rate='control',
            ...     )
            >>> ugen = control_bus_group.ar()
            >>> print(str(ugen))
            SynthDef ecaa7fe9417cb0742cdcda87657fe9de {
                const_0:8.0 -> 0_In[0:bus]
                0_In[0] -> 1_K2A[0:source]
                0_In[1] -> 2_K2A[0:source]
                0_In[2] -> 3_K2A[0:source]
                0_In[3] -> 4_K2A[0:source]
            }

        Returns ugen.
        '''
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        channel_count = len(self)
        if self.rate == synthdeftools.CalculationRate.AUDIO:
            ugen = ugentools.In.ar(
                bus=self.bus_id,
                channel_count=channel_count,
                )
        else:
            ugen = ugentools.In.kr(
                bus=self.bus_id,
                channel_count=channel_count,
                )
            ugen = ugentools.K2A.ar(
                source=ugen,
                )
        return ugen

    def free(self):
        from supriya.tools import servertools
        if not self.is_allocated:
            return
        allocator = servertools.Bus._get_allocator(
            rate=self.rate,
            server=self.server,
            )
        allocator.free(self.bus_id)
        self._bus_id = None
        ServerObjectProxy.free(self)

    def kr(self):
        r'''Creates a control-rate input ugen subgraph.

        ::

            >>> from supriya.tools import servertools
            >>> audio_bus_group = servertools.BusGroup(
            ...     bus_id=8,
            ...     bus_count=4,
            ...     rate='audio',
            ...     )
            >>> ugen = audio_bus_group.kr()
            >>> print(str(ugen))
            SynthDef ffeda833c370bc644251437469e243ef {
                const_0:8.0 -> 0_In[0:bus]
                0_In[0] -> 1_A2K[0:source]
                0_In[1] -> 2_A2K[0:source]
                0_In[2] -> 3_A2K[0:source]
                0_In[3] -> 4_A2K[0:source]
            }

        ::

            >>> control_bus_group = servertools.BusGroup(
            ...     bus_id=8,
            ...     bus_count=4,
            ...     rate='control',
            ...     )
            >>> ugen = control_bus_group.kr()
            >>> print(str(ugen))
            SynthDef b64857a04b384841694ba85f74f0fd0b {
                const_0:8.0 -> 0_In[0:bus]
            }

        Returns ugen.
        '''
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        channel_count = len(self)
        if self.rate == synthdeftools.CalculationRate.AUDIO:
            ugen = ugentools.In.ar(
                bus=self.bus_id,
                channel_count=channel_count,
                )
            ugen = ugentools.A2K.kr(
                source=ugen,
                )
        else:
            ugen = ugentools.In.kr(
                bus=self.bus_id,
                channel_count=channel_count,
                )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def buses(self):
        return self._buses

    @property
    def is_allocated(self):
        return self.server is not None

    @property
    def map_symbol(self):
        from supriya.tools import synthdeftools
        if self.rate == synthdeftools.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
        map_symbol += str(self.bus_id)
        return map_symbol

    @property
    def rate(self):
        return self._calculation_rate