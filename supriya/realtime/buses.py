import supriya.exceptions
from supriya import CalculationRate
from supriya.system import SupriyaValueObject

from .bases import ServerObject

# TODO: Reimplement Bus/BusGroup to stress "leasing" model


class Bus(ServerObject):
    """
    A bus.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> bus = supriya.Bus()
        >>> bus
        <- Bus: ??? (control)>

    ::

        >>> bus.allocate()
        <+ Bus: 0 (control)>

    ::

        >>> bus.get()
        0.0

    ::

        >>> bus.set(0.5)
        >>> bus.get()
        0.5

    ::

        >>> print(bus)
        c0

    ::

        >>> bus.free()
        <- Bus: ??? (control)>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_bus_group",
        "_bus_id",
        "_bus_id_was_set_manually",
        "_calculation_rate",
    )

    ### INITIALIZER ###

    def __init__(
        self, bus_group_or_index=None, calculation_rate=CalculationRate.CONTROL
    ):
        ServerObject.__init__(self)
        bus_group = None
        bus_id = None
        self._bus_id_was_set_manually = False
        if bus_group_or_index is not None:
            self._bus_id_was_set_manually = True
            if isinstance(bus_group_or_index, BusGroup):
                bus_group = bus_group_or_index
            elif isinstance(bus_group_or_index, int):
                bus_id = int(bus_group_or_index)
        self._bus_group = bus_group
        self._bus_id = bus_id
        if calculation_rate is None:
            calculation_rate = "control"
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        assert calculation_rate in (CalculationRate.AUDIO, CalculationRate.CONTROL)
        self._calculation_rate = calculation_rate

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.bus_id)

    def __int__(self):
        return int(self.bus_id)

    def __repr__(self):
        bus_id = self.bus_id
        if bus_id is None:
            bus_id = "???"
        return "<{} {}: {} ({})>".format(
            "+" if self.is_allocated else "-",
            type(self).__name__,
            bus_id,
            self.calculation_rate.name.lower(),
        )

    def __str__(self):
        """
        Gets map symbol representation of bus.

        ::

            >>> import supriya
            >>> server = supriya.Server.default().boot()
            >>> control_bus = server.add_bus("control")
            >>> audio_bus = server.add_bus("audio")

        ::

            >>> print(str(control_bus))
            c0

        ::

            >>> print(str(audio_bus))
            a16

        ::

            >>> print(str(control_bus.free()))
            Traceback (most recent call last):
            ...
            supriya.exceptions.BusNotAllocated

        """
        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated
        return self.map_symbol

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_allocator(calculation_rate=None, server=None):
        if calculation_rate == CalculationRate.AUDIO:
            allocator = server.audio_bus_allocator
        else:
            allocator = server.control_bus_allocator
        return allocator

    ### PUBLIC METHODS ###

    def allocate(self, server=None, sync=False):
        if self.bus_group is not None:
            return
        if self.is_allocated:
            raise supriya.exceptions.BusAlreadyAllocated
        ServerObject.allocate(self, server=server)
        if self.bus_id is None:
            allocator = self._get_allocator(
                calculation_rate=self.calculation_rate, server=self.server
            )
            bus_id = allocator.allocate(1)
            if bus_id is None:
                ServerObject.free(self)
                raise ValueError
            self._bus_id = bus_id
        if sync:
            self.server.sync()
        return self

    def free(self):
        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated
        if not self._bus_id_was_set_manually:
            allocator = self._get_allocator(
                calculation_rate=self.calculation_rate, server=self.server
            )
            allocator.free(self.bus_id)
        self._bus_id = None
        ServerObject.free(self)
        return self

    def get(self, completion_callback=None):
        import supriya.commands
        import supriya.realtime

        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated
        elif not self.calculation_rate == CalculationRate.CONTROL:
            raise supriya.exceptions.IncompatibleRate
        request = supriya.commands.ControlBusGetRequest(indices=(self,))
        if callable(completion_callback):
            raise NotImplementedError
        response = request.communicate(server=self.server)
        assert len(response) == 1
        value = response[0].bus_value
        return value

    def set(self, value):
        import supriya.commands
        import supriya.realtime

        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated
        elif not self.calculation_rate == CalculationRate.CONTROL:
            raise supriya.exceptions.IncompatibleRate
        request = supriya.commands.ControlBusSetRequest(
            index_value_pairs=((self, value),)
        )
        request.communicate(server=self.server, sync=False)

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
        if self.bus_id is None:
            raise supriya.exceptions.BusNotAllocated
        if self.calculation_rate == CalculationRate.AUDIO:
            map_symbol = "a"
        else:
            map_symbol = "c"
        map_symbol += str(self.bus_id)
        return map_symbol

    @property
    def server(self):
        if self.bus_group is not None:
            return self.bus_group.server
        return self._server

    @property
    def value(self):
        if self.is_allocated:
            if self.calculation_rate == CalculationRate.CONTROL:
                proxy = self.server._get_control_bus_proxy(self.bus_id)
                return proxy.value
        return None


class BusGroup(ServerObject):
    """
    A bus group.

    ::

        >>> server = supriya.Server.default().boot()
        >>> bus_group = supriya.BusGroup(bus_count=4)
        >>> bus_group
        <- BusGroup{4}: ??? (control)>

    ::

        >>> bus_group.allocate()
        <+ BusGroup{4}: 0 (control)>

    ::

        >>> bus_group[2]
        <+ Bus: 2 (control)>

    ::

        >>> for i in range(len(bus_group)):
        ...     bus = bus_group[i]
        ...     value = (i * 0.2) + 0.1
        ...     bus.set(value)
        ...
        >>> bus_values = bus_group.get()

    Values in ``scsynth`` don't necessarily have the same precision as in
    Python, so we'll round them here for display purposes:

    ::

        >>> print([round(value, 1) for value in bus_values])
        [0.1, 0.3, 0.5, 0.7]

    ::

        >>> print(bus_group)
        c0

    ::

        >>> bus_group.free()
        <- BusGroup{4}: ??? (control)>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_bus_id", "_buses", "_calculation_rate")

    ### INITIALIZER ###

    def __init__(
        self, bus_count=1, calculation_rate=CalculationRate.CONTROL, *, bus_id=None
    ):
        ServerObject.__init__(self)
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        assert calculation_rate in (CalculationRate.AUDIO, CalculationRate.CONTROL)
        self._calculation_rate = calculation_rate
        bus_count = int(bus_count)
        assert 0 < bus_count
        self._buses = tuple(
            Bus(bus_group_or_index=self, calculation_rate=self.calculation_rate)
            for _ in range(bus_count)
        )
        assert isinstance(bus_id, (type(None), int))
        self._bus_id = bus_id

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        """
        Test if a bus belongs to the bus group.

        ::

            >>> bus_group = supriya.BusGroup.control(4)
            >>> bus_group[0] in bus_group
            True

        ::

            >>> bus = supriya.Bus("audio")
            >>> bus in bus_group
            False

        """
        # TODO: Should this handle allocated buses that match by ID?
        return self.buses.__contains__(item)

    def __float__(self):
        return float(self.bus_id)

    def __getitem__(self, item):
        """
        Get ``item`` in bus group.

        ::

            >>> server = supriya.Server.default().boot()
            >>> bus_group = supriya.BusGroup.control(4).allocate()
            >>> bus_group[0]
            <+ Bus: 0 (control)>

        ::

            >>> bus_group[1:]
            <+ BusGroup{3}: 1 (control)>

        """
        if isinstance(item, int):
            return self._buses[item]
        elif isinstance(item, slice):
            indices = item.indices(len(self))
            bus_count = indices[1] - indices[0]
            bus_group = type(self)(
                bus_count=bus_count,
                bus_id=indices[0],
                calculation_rate=self.calculation_rate,
            )
            if self.is_allocated:
                bus_group._server = self.server
            return bus_group

    def __int__(self):
        return int(self.bus_id)

    def __iter__(self):
        return iter(self.buses)

    def __len__(self):
        return len(self._buses)

    def __repr__(self):
        bus_id = self.bus_id
        if bus_id is None:
            bus_id = "???"
        return "<{} {}{{{}}}: {} ({})>".format(
            "+" if self.is_allocated else "-",
            type(self).__name__,
            len(self),
            bus_id,
            self.calculation_rate.name.lower(),
        )

    def __str__(self):
        """
        Gets map symbol representation of bus group.

        ::

            >>> server = supriya.Server.default().boot()
            >>> control_bus_group = server.add_bus_group(4, "control")
            >>> audio_bus_group = server.add_bus_group(4, "audio")

        ::

            >>> print(str(control_bus_group))
            c0

        ::

            >>> print(str(audio_bus_group))
            a16

        """
        return self.map_symbol

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        if self.is_allocated:
            raise supriya.exceptions.BusAlreadyAllocated
        ServerObject.allocate(self, server=server)
        allocator = Bus._get_allocator(
            calculation_rate=self.calculation_rate, server=self.server
        )
        bus_id = allocator.allocate(len(self))
        if bus_id is None:
            ServerObject.free(self)
            raise ValueError
        self._bus_id = bus_id
        return self

    def ar(self):
        """
        Creates an audio-rate input ugen subgraph.

        ..  container:: example

            ::

                >>> import supriya.realtime
                >>> audio_bus_group = supriya.realtime.BusGroup(
                ...     bus_id=8, bus_count=4, calculation_rate="audio",
                ... )
                >>> ugen = audio_bus_group.ar()
                >>> supriya.graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: 0af6b551a643cad01e9994845ff4ae40
                    ugens:
                    -   In.ar:
                            bus: 8.0

        ..  container:: example

            ::

                >>> control_bus_group = supriya.realtime.BusGroup(
                ...     bus_id=8, bus_count=4, calculation_rate="control",
                ... )
                >>> ugen = control_bus_group.ar()
                >>> supriya.graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: ecaa7fe9417cb0742cdcda87657fe9de
                    ugens:
                    -   In.kr:
                            bus: 8.0
                    -   K2A.ar/0:
                            source: In.kr[0]
                    -   K2A.ar/1:
                            source: In.kr[1]
                    -   K2A.ar/2:
                            source: In.kr[2]
                    -   K2A.ar/3:
                            source: In.kr[3]

        Returns ugen.
        """
        import supriya.ugens

        channel_count = len(self)
        if self.calculation_rate == CalculationRate.AUDIO:
            ugen = supriya.ugens.In.ar(bus=self.bus_id, channel_count=channel_count)
        else:
            ugen = supriya.ugens.In.kr(bus=self.bus_id, channel_count=channel_count)
            ugen = supriya.ugens.K2A.ar(source=ugen)
        return ugen

    @classmethod
    def audio(cls, bus_count=1):
        return cls(bus_count=bus_count, calculation_rate=CalculationRate.AUDIO)

    @classmethod
    def control(cls, bus_count=1):
        return cls(bus_count=bus_count, calculation_rate=CalculationRate.CONTROL)

    def fill(self, value):
        """
        Fill buses in bus group with ``value``.

        ::

            >>> server = supriya.Server.default().boot()
            >>> bus_group = server.add_bus_group(4, "control")
            >>> bus_group.get()
            (0.0, 0.0, 0.0, 0.0)

        ::

            >>> bus_group.fill(0.5)

        ::

            >>> bus_group.get()
            (0.5, 0.5, 0.5, 0.5)

        ::

            >>> bus_group = supriya.BusGroup(4, "audio")
            >>> bus_group.fill(0.5)
            Traceback (most recent call last):
            ...
            supriya.exceptions.BusNotAllocated

        ::

            >>> bus_group.allocate().fill(0.5)
            Traceback (most recent call last):
            ...
            supriya.exceptions.IncompatibleRate

        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated
        if self.calculation_rate != CalculationRate.CONTROL:
            raise supriya.exceptions.IncompatibleRate
        index_count_value_triples = [(self.bus_id, len(self), value)]
        request = supriya.commands.ControlBusFillRequest(
            index_count_value_triples=index_count_value_triples
        )
        request.communicate(server=self.server, sync=False)

    def free(self):
        if not self.is_allocated:
            return
        allocator = Bus._get_allocator(
            calculation_rate=self.calculation_rate, server=self.server
        )
        if allocator:
            allocator.free(self.bus_id)
        self._bus_id = None
        ServerObject.free(self)
        return self

    def get(self):
        """
        Get bus group values.

        ::

            >>> server = supriya.Server.default().boot()
            >>> bus_group = supriya.BusGroup().control(4).allocate()
            >>> bus_group.get()
            (0.0, 0.0, 0.0, 0.0)

        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated
        if self.calculation_rate != CalculationRate.CONTROL:
            raise supriya.exceptions.IncompatibleRate
        index_count_pairs = [(self.bus_id, len(self))]
        request = supriya.commands.ControlBusGetContiguousRequest(
            index_count_pairs=index_count_pairs
        )
        response = request.communicate(server=self.server)
        assert len(response) == 1
        value = response[0].bus_values
        return value

    def index(self, item):
        return self.buses.index(item)

    def kr(self):
        """
        Creates a control-rate input ugen subgraph.

        ..  container:: example

            ::

                >>> import supriya.realtime
                >>> audio_bus_group = supriya.realtime.BusGroup(
                ...     bus_id=8, bus_count=4, calculation_rate="audio",
                ... )
                >>> ugen = audio_bus_group.kr()
                >>> supriya.graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: ffeda833c370bc644251437469e243ef
                    ugens:
                    -   In.ar:
                            bus: 8.0
                    -   A2K.kr/0:
                            source: In.ar[0]
                    -   A2K.kr/1:
                            source: In.ar[1]
                    -   A2K.kr/2:
                            source: In.ar[2]
                    -   A2K.kr/3:
                            source: In.ar[3]

        ..  container:: example

            ::

                >>> control_bus_group = supriya.realtime.BusGroup(
                ...     bus_id=8, bus_count=4, calculation_rate="control",
                ... )
                >>> ugen = control_bus_group.kr()
                >>> supriya.graph(ugen)  # doctest: +SKIP

            ::

                >>> print(ugen)
                synthdef:
                    name: b64857a04b384841694ba85f74f0fd0b
                    ugens:
                    -   In.kr:
                            bus: 8.0

        Returns ugen.
        """
        import supriya.ugens

        channel_count = len(self)
        if self.calculation_rate == CalculationRate.AUDIO:
            ugen = supriya.ugens.In.ar(bus=self.bus_id, channel_count=channel_count)
            ugen = supriya.ugens.A2K.kr(source=ugen)
        else:
            ugen = supriya.ugens.In.kr(bus=self.bus_id, channel_count=channel_count)
        return ugen

    def set(self, values):
        """
        Set bus group values.

        ::

            >>> server = supriya.Server.default().boot()
            >>> bus_group = supriya.BusGroup.control(4).allocate()
            >>> bus_group.get()
            (0.0, 0.0, 0.0, 0.0)

        ::

            >>> bus_group.set((-0.5, 0.5, -0.5, 0.5))
            >>> bus_group.get()
            (-0.5, 0.5, -0.5, 0.5)

        """
        import supriya.commands

        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated(self)
        if self.calculation_rate != CalculationRate.CONTROL:
            raise supriya.exceptions.IncompatibleRate(self)
        if len(values) != len(self):
            raise ValueError(values)
        request = supriya.commands.ControlBusSetContiguousRequest(
            index_values_pairs=[(self, values)]
        )
        request.communicate(sync=False)

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def buses(self):
        return self._buses

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def is_allocated(self):
        return self.server is not None

    @property
    def map_symbol(self):
        if self.bus_id is None:
            raise supriya.exceptions.BusNotAllocated
        if self.calculation_rate == CalculationRate.AUDIO:
            map_symbol = "a"
        else:
            map_symbol = "c"
        map_symbol += str(self.bus_id)
        return map_symbol


class BusProxy(SupriyaValueObject):
    """
    A buffer proxy.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_bus_id", "_calculation_rate", "_server", "_value")

    ### INITIALIZER ###

    def __init__(self, bus_id=None, calculation_rate=None, server=None, value=0.0):
        import supriya.realtime
        import supriya.synthdefs

        bus_id = int(bus_id)
        assert 0 <= bus_id
        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        assert isinstance(server, supriya.realtime.Server)
        self._bus_id = int(bus_id)
        self._calculation_rate = calculation_rate
        self._server = server
        self._value = value or 0.0

    ### SPECIAL METHODS ###

    def __float__(self):
        return float(self.bus_id)

    def __int__(self):
        return int(self.bus_id)

    def __str__(self):
        return self.map_symbol

    ### PUBLIC PROPERTIES ###

    @property
    def bus_id(self):
        return self._bus_id

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def map_symbol(self):
        import supriya.synthdefs

        if self.calculation_rate == supriya.CalculationRate.AUDIO:
            map_symbol = "a"
        else:
            map_symbol = "c"
        map_symbol += str(self.bus_id)
        return map_symbol

    @property
    def server(self):
        return self._server

    @property
    def value(self):
        return self._value


class AudioInputBusGroup(BusGroup):
    """
    Audio input bus group.

    Allocated automatically on server boot.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> bus_group = server.audio_input_bus_group
        >>> bus_group
        <+ AudioInputBusGroup{8}: 8 (audio)>

    ::

        >>> bus_group.is_allocated
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, server):
        import supriya.realtime
        import supriya.synthdefs

        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        BusGroup.__init__(
            self,
            bus_count=server.options.input_bus_channel_count,
            calculation_rate=supriya.CalculationRate.AUDIO,
        )
        self._bus_id = server.options.output_bus_channel_count
        self._server = server

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass


class AudioOutputBusGroup(BusGroup):
    """
    Audio output bus group.

    Allocated automatically on server boot.

    ::

        >>> import supriya
        >>> server = supriya.Server.default().boot()
        >>> bus_group = server.audio_output_bus_group
        >>> bus_group
        <+ AudioOutputBusGroup{8}: 0 (audio)>

    ::

        >>> bus_group.is_allocated
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, server):
        import supriya.realtime
        import supriya.synthdefs

        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        BusGroup.__init__(
            self,
            bus_count=server.options.input_bus_channel_count,
            calculation_rate=supriya.CalculationRate.AUDIO,
        )
        self._bus_id = 0
        self._server = server

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass
