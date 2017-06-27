from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class Bus(ServerObjectProxy):
    """
    A bus.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_bus_group',
        '_bus_id',
        '_bus_id_was_set_manually',
        '_calculation_rate',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bus_group_or_index=None,
        calculation_rate=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        bus_group = None
        bus_id = None
        self._bus_id_was_set_manually = False
        if bus_group_or_index is not None:
            self._bus_id_was_set_manually = True
            if isinstance(bus_group_or_index, servertools.BusGroup):
                bus_group = bus_group_or_index
            elif isinstance(bus_group_or_index, int):
                bus_id = int(bus_group_or_index)
        self._bus_group = bus_group
        self._bus_id = bus_id
        assert calculation_rate is not None
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        self._calculation_rate = calculation_rate

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.bus_id)

    def __int__(self):
        return int(self.bus_id)

    def __repr__(self):
        string = '<{}: {}>'.format(
            type(self).__name__,
            self.bus_id,
            )
        return string

    def __str__(self):
        return self.map_symbol

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_allocator(
        calculation_rate=None,
        server=None,
        ):
        from supriya.tools import synthdeftools
        if calculation_rate == synthdeftools.CalculationRate.AUDIO:
            allocator = server.audio_bus_allocator
        else:
            allocator = server.control_bus_allocator
        return allocator

    def _receive_bound_event(self, event=None):
        if event is None:
            return
        event = float(event)
        self.set(event)

    ### PUBLIC METHODS ###

    def allocate(
        self,
        server=None,
        sync=False,
        ):
        if self.bus_group is not None:
            return
        if self.is_allocated:
            return
        ServerObjectProxy.allocate(self, server=server)
        if self.bus_id is None:
            allocator = self._get_allocator(
                calculation_rate=self.calculation_rate,
                server=self.server,
                )
            bus_id = allocator.allocate(1)
            if bus_id is None:
                ServerObjectProxy.free(self)
                raise ValueError
            self._bus_id = bus_id
        if sync:
            self.server.sync()
        return self

    def ar(self):
        """
        Creates an audio-rate input ugen subgraph.

        ::

            >>> from supriya.tools import servertools
            >>> audio_bus = servertools.Bus(8, 'audio')
            >>> ugen = audio_bus.ar()
            >>> print(str(ugen))
            SynthDef fb63450852ac2df2fad1242e27a913d6 {
                const_0:8.0 -> 0_In[0:bus]
            }

        ::

            >>> control_bus = servertools.Bus(8, 'control')
            >>> ugen = control_bus.ar()
            >>> print(str(ugen))
            SynthDef d48f76506e364201100db95a248cc8e2 {
                const_0:8.0 -> 0_In[0:bus]
                0_In[0] -> 1_K2A[0:source]
            }

        Returns ugen.
        """
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        channel_count = 1
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
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

    @staticmethod
    def audio():
        from supriya.tools import synthdeftools
        return Bus(
            calculation_rate=synthdeftools.CalculationRate.AUDIO,
            )

    @staticmethod
    def control():
        from supriya.tools import synthdeftools
        return Bus(
            calculation_rate=synthdeftools.CalculationRate.CONTROL,
            )

    def free(self):
        if not self.is_allocated:
            return
        if not self._bus_id_was_set_manually:
            allocator = self._get_allocator(
                calculation_rate=self.calculation_rate,
                server=self.server,
                )
            allocator.free(self.bus_id)
        self._bus_id = None
        ServerObjectProxy.free(self)

    def get(
        self,
        completion_callback=None,
        ):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        if not self.is_allocated:
            raise servertools.NotAllocatedError(self)
        elif not self.calculation_rate == synthdeftools.CalculationRate.CONTROL:
            raise synthdeftools.RateError
        request = requesttools.ControlBusGetRequest(
            indices=(self,),
            )
        if callable(completion_callback):
            raise NotImplementedError
        response = request.communicate(server=self.server)
        assert len(response) == 1
        value = response[0].bus_value
        return value

    def kr(self):
        """
        Creates a control-rate input ugen subgraph.

        ::

            >>> from supriya.tools import servertools
            >>> audio_bus = servertools.Bus(8, 'audio')
            >>> ugen = audio_bus.kr()
            >>> print(str(ugen))
            SynthDef 65ceebd3294ae43fa3dd12035e1895fd {
                const_0:8.0 -> 0_In[0:bus]
                0_In[0] -> 1_A2K[0:source]
            }

        ::

            >>> control_bus = servertools.Bus(8, 'control')
            >>> ugen = control_bus.kr()
            >>> print(str(ugen))
            SynthDef ef2c11e55da5af28e2ae77c5c8934f3d {
                const_0:8.0 -> 0_In[0:bus]
            }

        Returns ugen.
        """
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        channel_count = 1
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
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

    def set(self, value):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        if not self.is_allocated:
            raise servertools.NotAllocatedError(self)
        elif not self.calculation_rate == synthdeftools.CalculationRate.CONTROL:
            raise synthdeftools.RateError
        request = requesttools.ControlBusSetRequest(
            index_value_pairs=((self, value,),),
            )
        request.communicate(
            server=self.server,
            sync=False,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def bus_group(self):
        return self._bus_group

    @property
    def bus_id(self):
        if self._bus_group is not None:
            if self._bus_group.bus_id is not None:
                group_id = self._bus_group.bus_id
                index = self._bus_group.index(self)
                bus_id = group_id + index
                return bus_id
        return self._bus_id

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def is_allocated(self):
        if self.bus_group is not None:
            return self.bus_group.is_allocated
        return self.server is not None

    @property
    def map_symbol(self):
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            map_symbol = 'a'
        else:
            map_symbol = 'c'
        map_symbol += str(self.bus_id)
        return map_symbol

    @property
    def server(self):
        if self.bus_group is not None:
            return self.bus_group.server
        return self._server

    @property
    def value(self):
        from supriya.tools import synthdeftools
        if self.is_allocated:
            if self.calculation_rate == synthdeftools.CalculationRate.CONTROL:
                proxy = self.server._get_control_bus_proxy(self.bus_id)
                return proxy.value
        return None
