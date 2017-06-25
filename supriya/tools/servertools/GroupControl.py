from supriya.tools.bindingtools.BindingTarget import BindingTarget


class GroupControl(BindingTarget):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_binding_sources',
        '_client',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        name=None,
        ):
        BindingTarget.__init__(self)
        self._client = client
        self._name = str(name)

    ### SPECIAL METHODS ###

    def __str__(self):
        return self.name

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(
            client=self,
            storage_format_kwargs_names=['name'],
            )

    def _map_to_bus(self, bus):
        pass

    def _receive_bound_event(self, event=None):
        if event is None:
            return
        event = float(event)
        self.set(event)

    def _set_to_number(self, value):
        pass

    def _unmap(self):
        pass

    ### PUBLIC METHODS ###

    def set(self, expr):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        if isinstance(expr, servertools.Bus):
            if expr.calculation_rate == synthdeftools.CalculationRate.CONTROL:
                request = requesttools.NodeMapToControlBusRequest(
                    self.node,
                    **{self.name: expr}
                    )
            else:
                request = requesttools.NodeMapToAudioBusRequest(
                    self.node,
                    **{self.name: expr}
                    )
        else:
            expr = float(expr)
            request = requesttools.NodeSetRequest(
                self.node,
                **{self.name: expr}
                )
        if self.node.is_allocated:
            request.communicate(server=self.node.server)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def group(self):
        return self.client.client

    @property
    def name(self):
        return self._name

    @property
    def node(self):
        return self.client.client
