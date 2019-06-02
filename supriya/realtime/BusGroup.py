import supriya.exceptions
from supriya import CalculationRate
from supriya.realtime.ServerObject import ServerObject


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

    __documentation_section__ = "Main Classes"

    __slots__ = ("_bus_id", "_buses", "_calculation_rate")

    ### INITIALIZER ###

    def __init__(
        self, bus_count=1, calculation_rate=CalculationRate.CONTROL, *, bus_id=None
    ):
        import supriya.realtime

        ServerObject.__init__(self)
        calculation_rate = CalculationRate.from_expr(calculation_rate)
        assert calculation_rate in (CalculationRate.AUDIO, CalculationRate.CONTROL)
        self._calculation_rate = calculation_rate
        bus_count = int(bus_count)
        assert 0 < bus_count
        self._buses = tuple(
            supriya.realtime.Bus(
                bus_group_or_index=self, calculation_rate=self.calculation_rate
            )
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

            >>> bus = supriya.Bus.audio()
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
            >>> control_bus_group = supriya.BusGroup.control(4).allocate()
            >>> audio_bus_group = supriya.BusGroup.audio(4).allocate()

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
        import supriya.realtime

        if self.is_allocated:
            raise supriya.exceptions.BusAlreadyAllocated
        ServerObject.allocate(self, server=server)
        allocator = supriya.realtime.Bus._get_allocator(
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
                ...     bus_id=8,
                ...     bus_count=4,
                ...     calculation_rate='audio',
                ...     )
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
                ...     bus_id=8,
                ...     bus_count=4,
                ...     calculation_rate='control',
                ...     )
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
            >>> bus_group = supriya.BusGroup.control(4).allocate()
            >>> bus_group.get()
            (0.0, 0.0, 0.0, 0.0)

        ::

            >>> bus_group.fill(0.5)

        ::

            >>> bus_group.get()
            (0.5, 0.5, 0.5, 0.5)

        ::

            >>> bus_group = supriya.BusGroup.audio(4)
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
        import supriya.realtime

        if not self.is_allocated:
            raise supriya.exceptions.BusNotAllocated
        allocator = supriya.realtime.Bus._get_allocator(
            calculation_rate=self.calculation_rate, server=self.server
        )
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
                ...     bus_id=8,
                ...     bus_count=4,
                ...     calculation_rate='audio',
                ...     )
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
                ...     bus_id=8,
                ...     bus_count=4,
                ...     calculation_rate='control',
                ...     )
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
