class ServerSession(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_bus_allocator',
        '_audio_busses',
        '_buffer_allocator',
        '_buffers',
        '_control_bus_allocator',
        '_control_busses',
        '_default_group',
        '_node_id_allocator',
        '_nodes',
        '_root_node',
        '_server_options',
        '_server_process',
        '_synth_definitions',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        server_options=None,
        server_process=None,
        ):
        from supriya.library import controllib
        server_options = server_options or controllib.ServerOptions()
        assert isinstance(server_options, controllib.ServerOptions)
        self._server_options = server_options
        self._server_process = server_process

        self._audio_bus_allocator = controllib.BlockAllocator()
        self._buffer_allocator = controllib.BlockAllocator()
        self._control_bus_allocator = controllib.BlockAllocator()
        self._node_id_allocator = controllib.NodeIDAllocator()

        self._audio_busses = {}
        self._buffers = {}
        self._control_busses = {}
        self._nodes = {}
        self._synth_definitions = {}

        self._root_node = controllib.RootNode()
        self._default_group = controllib.DefaultGroup()
        self._default_group._parent_group = self._root_node

    ### PUBLIC METHODS ###

    def free(self):
        for x in self.audio_busses.values():
            x.free()
        for x in self.buffers.values():
            x.free()
        for x in self.control_busses.values():
            x.free()
        for x in self.nodes.values():
            x.free()

    ### PUBLIC PROPERTIES ###

    @property
    def audio_bus_allocator(self):
        return self._audio_bus_allocator

    @property
    def audio_busses(self):
        return self._audio_busses

    @property
    def buffer_allocator(self):
        return self._buffer_allocator

    @property
    def buffers(self):
        return self._buffers

    @property
    def control_bus_allocator(self):
        return self._control_bus_allocator

    @property
    def control_busses(self):
        return self._control_busses

    @property
    def node_id_allocator(self):
        return self._node_id_allocator

    @property
    def nodes(self):
        return self._nodes

    @property
    def root_node(self):
        return self._root_node

    @property
    def server_options(self):
        return self._server_options

    @property
    def server_process(self):
        return self._server_process

    @property
    def synth_definitions(self):
        return self._synth_definitions
