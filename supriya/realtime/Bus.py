from supriya.realtime.ServerObjectProxy import ServerObjectProxy


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
        import supriya.realtime
        import supriya.synthdefs
        ServerObjectProxy.__init__(self)
        bus_group = None
        bus_id = None
        self._bus_id_was_set_manually = False
        if bus_group_or_index is not None:
            self._bus_id_was_set_manually = True
            if isinstance(bus_group_or_index, supriya.realtime.BusGroup):
                bus_group = bus_group_or_index
            elif isinstance(bus_group_or_index, int):
                bus_id = int(bus_group_or_index)
        self._bus_group = bus_group
        self._bus_id = bus_id
        if calculation_rate is None:
            calculation_rate = 'control'
        calculation_rate = supriya.synthdefs.CalculationRate.from_expr(
            calculation_rate)
        assert calculation_rate in (
            supriya.synthdefs.CalculationRate.AUDIO,
            supriya.synthdefs.CalculationRate.CONTROL,
            )
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
        import supriya.synthdefs
        if calculation_rate == supriya.synthdefs.CalculationRate.AUDIO:
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

        ..  container:: example

            ::

                >>> import supriya.realtime
                >>> audio_bus = supriya.realtime.Bus(8, 'audio')
                >>> ugen = audio_bus.ar()
                >>> graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: fb63450852ac2df2fad1242e27a913d6
                    ugens:
                    -   In.ar:
                            bus: 8.0

        ..  container:: example

            ::

                >>> control_bus = supriya.realtime.Bus(8, 'control')
                >>> ugen = control_bus.ar()
                >>> graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: d48f76506e364201100db95a248cc8e2
                    ugens:
                    -   In.kr:
                            bus: 8.0
                    -   K2A.ar:
                            source: In.kr[0]

        Returns ugen.
        """
        import supriya.synthdefs
        import supriya.ugens
        channel_count = 1
        if self.calculation_rate == supriya.synthdefs.CalculationRate.AUDIO:
            ugen = supriya.ugens.In.ar(
                bus=self.bus_id,
                channel_count=channel_count,
                )
        else:
            ugen = supriya.ugens.In.kr(
                bus=self.bus_id,
                channel_count=channel_count,
                )
            ugen = supriya.ugens.K2A.ar(
                source=ugen,
                )
        return ugen

    @staticmethod
    def audio():
        import supriya.synthdefs
        return Bus(
            calculation_rate=supriya.synthdefs.CalculationRate.AUDIO,
            )

    @staticmethod
    def control():
        import supriya.synthdefs
        return Bus(
            calculation_rate=supriya.synthdefs.CalculationRate.CONTROL,
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
        import supriya.commands
        import supriya.realtime
        import supriya.synthdefs
        if not self.is_allocated:
            raise supriya.realtime.NotAllocatedError(self)
        elif not self.calculation_rate == supriya.synthdefs.CalculationRate.CONTROL:
            raise supriya.synthdefs.RateError
        request = supriya.commands.ControlBusGetRequest(
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

        ..  container:: example

            ::

                >>> import supriya.realtime
                >>> audio_bus = supriya.realtime.Bus(8, 'audio')
                >>> ugen = audio_bus.kr()
                >>> graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: 65ceebd3294ae43fa3dd12035e1895fd
                    ugens:
                    -   In.ar:
                            bus: 8.0
                    -   A2K.kr:
                            source: In.ar[0]

        ..  container:: example

            ::

                >>> control_bus = supriya.realtime.Bus(8, 'control')
                >>> ugen = control_bus.kr()
                >>> graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: ef2c11e55da5af28e2ae77c5c8934f3d
                    ugens:
                    -   In.kr:
                            bus: 8.0

        Returns ugen.
        """
        import supriya.synthdefs
        import supriya.ugens
        channel_count = 1
        if self.calculation_rate == supriya.synthdefs.CalculationRate.AUDIO:
            ugen = supriya.ugens.In.ar(
                bus=self.bus_id,
                channel_count=channel_count,
                )
            ugen = supriya.ugens.A2K.kr(
                source=ugen,
                )
        else:
            ugen = supriya.ugens.In.kr(
                bus=self.bus_id,
                channel_count=channel_count,
                )
        return ugen

    def set(self, value):
        import supriya.commands
        import supriya.realtime
        import supriya.synthdefs
        if not self.is_allocated:
            raise supriya.realtime.NotAllocatedError(self)
        elif not self.calculation_rate == supriya.synthdefs.CalculationRate.CONTROL:
            raise supriya.synthdefs.RateError
        request = supriya.commands.ControlBusSetRequest(
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
        import supriya.synthdefs
        if self.calculation_rate == supriya.synthdefs.CalculationRate.AUDIO:
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
        import supriya.synthdefs
        if self.is_allocated:
            if self.calculation_rate == supriya.synthdefs.CalculationRate.CONTROL:
                proxy = self.server._get_control_bus_proxy(self.bus_id)
                return proxy.value
        return None
