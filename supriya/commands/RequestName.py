from uqbar.enums import StrictEnumeration


class RequestName(StrictEnumeration):
    """
    An enumeration of scsynth request names.
    """

    ### CLASS VARIABLES ###

    BUFFER_ALLOCATE = '/b_alloc'
    BUFFER_ALLOCATE_READ = '/b_allocRead'
    BUFFER_ALLOCATE_READ_CHANNEL = '/b_allocReadChannel'
    BUFFER_CLOSE = '/b_close'
    BUFFER_FILL = '/b_fill'
    BUFFER_FREE = '/b_free'
    BUFFER_GENERATE = '/b_gen'
    BUFFER_GET = '/b_get'
    BUFFER_GET_CONTIGUOUS = '/b_getn'
    BUFFER_QUERY = '/b_query'
    BUFFER_READ = '/b_read'
    BUFFER_READ_CHANNEL = '/b_readChannel'
    BUFFER_SET = '/b_set'
    BUFFER_SET_CONTIGUOUS = '/b_setn'
    BUFFER_WRITE = '/b_write'
    BUFFER_ZERO = '/b_zero'
    CLEAR_SCHEDULE = '/clearSched'
    COMMAND = '/cmd'
    CONTROL_BUS_FILL = '/c_fill'
    CONTROL_BUS_GET = '/c_get'
    CONTROL_BUS_GET_CONTIGUOUS = '/c_getn'
    CONTROL_BUS_SET = '/c_set'
    CONTROL_BUS_SET_CONTIGUOUS = '/c_setn'
    DUMP_OSC = '/dumpOSC'
    ERROR = '/error'
    GROUP_DEEP_FREE = '/g_deepFree'
    GROUP_DUMP_TREE = '/g_dumpTree'
    GROUP_FREE_ALL = '/g_freeAll'
    GROUP_HEAD = '/g_head'
    GROUP_NEW = '/g_new'
    GROUP_QUERY_TREE = '/g_queryTree'
    GROUP_TAIL = '/g_tail'
    NODE_AFTER = '/n_after'
    NODE_BEFORE = '/n_before'
    # NODE_COMMAND = None
    NODE_FILL = '/n_fill'
    NODE_FREE = '/n_free'
    NODE_MAP_TO_AUDIO_BUS = '/n_mapa'
    NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS = '/n_mapan'
    NODE_MAP_TO_CONTROL_BUS = '/n_map'
    NODE_MAP_TO_CONTROL_BUS_CONTIGUOUS = '/n_mapn'
    NODE_ORDER = '/n_order'
    NODE_QUERY = '/n_query'
    NODE_RUN = '/n_run'
    NODE_SET = '/n_set'
    NODE_SET_CONTIGUOUS = '/n_setn'
    NODE_TRACE = '/n_trace'
    # NOTHING = None
    NOTIFY = '/notify'
    PARALLEL_GROUP_NEW = '/p_new'
    QUIT = '/quit'
    STATUS = '/status'
    SYNC = '/sync'
    SYNTHDEF_FREE = '/d_free'
    # SYNTHDEF_FREE_ALL = None
    SYNTHDEF_LOAD = '/d_load'
    SYNTHDEF_LOAD_DIR = '/d_loadDir'
    SYNTHDEF_RECEIVE = '/d_recv'
    SYNTH_GET = '/s_get'
    SYNTH_GET_CONTIGUOUS = '/s_getn'
    SYNTH_NEW = '/s_new'
    # SYNTH_NEWARGS = None
    SYNTH_NOID = '/s_noid'
    UGEN_COMMAND = '/u_cmd'

    ### PUBLIC PROPERTIES ###

    @property
    def request_id(self):
        from supriya.commands import RequestId
        return RequestId.from_expr(self.name)
