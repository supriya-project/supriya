class ServerSession(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio_bus_allocator',
        '_buffer_allocator',
        '_control_bus_allocator',
        '_node_id_allocator',
        '_root_node',
        '_server_options',
        '_server_process',
        '_synth_definitions',
        )

    ### INITIALIZER ###

    def __init__(self, server_options=None):
        from supriya.library import controllib
        server_options = server_options or controllib.ServerOptions()
        assert isinstance(server_options, controllib.ServerOptions)
        self._server_options = server_options
        self._audio_bus_allocator = controllib.BlockAllocator()
        self._buffer_allocator = controllib.BlockAllocator()
        self._control_bus_allocator = controllib.BlockAllocator()
        self._node_id_allocator = controllib.NodeIDAllocator()
        self._root_node = controllib.RootNode()
        self._server_process = None
        self._synth_definitions = {}

    ### PUBLIC PROPERTIES ###

    @property
    def audio_bus_allocator(self):
        return self._audio_bus_allocator

    @property
    def buffer_allocator(self):
        return self._buffer_allocator

    @property
    def control_bus_allocator(self):
        return self._control_bus_allocator

    @property
    def node_id_allocator(self):
        return self._node_id_allocator

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
