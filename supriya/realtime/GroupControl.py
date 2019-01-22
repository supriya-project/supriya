class GroupControl:

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ("_client", "_name")

    ### INITIALIZER ###

    def __init__(self, client=None, name=None):
        self._client = client
        self._name = str(name)

    ### SPECIAL METHODS ###

    def __repr__(self):
        class_name = type(self).__name__
        calculation_rates = sorted(
            set(
                synth.controls[self.name].calculation_rate
                for synth in self.client._synth_controls["amplitude"]
            )
        )
        return '<{}: {!r} "{}" [{}]>'.format(
            class_name,
            self.client.client,
            self.name,
            ", ".join(_.token for _ in calculation_rates),
        )

    def __str__(self):
        return self.name

    ### PRIVATE METHODS ###

    def _map_to_bus(self, bus):
        pass

    def _set_to_number(self, number):
        pass

    def _unmap(self):
        pass

    ### PUBLIC METHODS ###

    def set(self, expr):
        self._client[self.name] = expr

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
