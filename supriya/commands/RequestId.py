from uqbar.enums import IntEnumeration


class RequestId(IntEnumeration):
    """
    An enumeration of scsynth message types.
    """

    ### CLASS VARIABLES ###

    BUFFER_ALLOCATE = 28
    BUFFER_ALLOCATE_READ = 29
    BUFFER_ALLOCATE_READ_CHANNEL = 54
    BUFFER_CLOSE = 33
    BUFFER_FILL = 37
    BUFFER_FREE = 32
    BUFFER_GENERATE = 38
    BUFFER_GET = 42
    BUFFER_GET_CONTIGUOUS = 43
    BUFFER_QUERY = 47
    BUFFER_READ = 30
    BUFFER_READ_CHANNEL = 55
    BUFFER_SET = 35
    BUFFER_SET_CONTIGUOUS = 36
    BUFFER_WRITE = 31
    BUFFER_ZERO = 34
    CLEAR_SCHEDULE = 51
    COMMAND = 4
    CONTROL_BUS_FILL = 27
    CONTROL_BUS_GET = 40
    CONTROL_BUS_GET_CONTIGUOUS = 41
    CONTROL_BUS_SET = 25
    CONTROL_BUS_SET_CONTIGUOUS = 26
    DUMP_OSC = 39
    ERROR = 58
    GROUP_DEEP_FREE = 50
    GROUP_DUMP_TREE = 56
    GROUP_FREE_ALL = 24
    GROUP_HEAD = 22
    GROUP_NEW = 21
    GROUP_QUERY_TREE = 57
    GROUP_TAIL = 23
    NODE_AFTER = 19
    NODE_BEFORE = 18
    NODE_COMMAND = 13
    NODE_FILL = 17
    NODE_FREE = 11
    NODE_MAP_TO_CONTROL_BUS = 14
    NODE_MAP_TO_AUDIO_BUS = 60
    NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS = 61
    NODE_MAP_TO_CONTROL_BUS_CONTIGUOUS = 48
    NODE_ORDER = 62
    NODE_QUERY = 46
    NODE_RUN = 12
    NODE_SET = 15
    NODE_SET_CONTIGUOUS = 16
    NODE_TRACE = 10
    NOTHING = 0
    NOTIFY = 1
    PARALLEL_GROUP_NEW = 63
    QUIT = 3
    STATUS = 2
    SYNC = 52
    SYNTHDEF_FREE = 53
    SYNTHDEF_FREE_ALL = 8
    SYNTHDEF_LOAD = 6
    SYNTHDEF_LOAD_DIR = 7
    SYNTHDEF_RECEIVE = 5
    SYNTH_GET = 44
    SYNTH_GET_CONTIGUOUS = 45
    SYNTH_NEW = 9
    SYNTH_NEWARGS = 59
    SYNTH_NOID = 49
    UGEN_COMMAND = 20

    @property
    def osc_command(self):
        return self._osc_commands.get(self) or self.value


RequestId._osc_commands = {
    RequestId.BUFFER_ALLOCATE: '/b_alloc',
    RequestId.BUFFER_ALLOCATE_READ: '/b_allocRead',
    RequestId.BUFFER_ALLOCATE_READ_CHANNEL: '/b_allocReadChannel',
    RequestId.BUFFER_CLOSE: '/b_close',
    RequestId.BUFFER_FILL: '/b_fill',
    RequestId.BUFFER_FREE: '/b_free',
    RequestId.BUFFER_GENERATE: '/b_gen',
    RequestId.BUFFER_GET: '/b_get',
    RequestId.BUFFER_GET_CONTIGUOUS: '/b_getn',
    RequestId.BUFFER_QUERY: '/b_query',
    RequestId.BUFFER_READ: '/b_read',
    RequestId.BUFFER_READ_CHANNEL: '/b_readChannel',
    RequestId.BUFFER_SET: '/b_set',
    RequestId.BUFFER_SET_CONTIGUOUS: '/b_setn',
    RequestId.BUFFER_WRITE: '/b_write',
    RequestId.BUFFER_ZERO: '/b_zero',
    RequestId.CLEAR_SCHEDULE: '/clearSched',
    RequestId.COMMAND: '/cmd',
    RequestId.CONTROL_BUS_FILL: '/c_fill',
    RequestId.CONTROL_BUS_GET: '/c_get',
    RequestId.CONTROL_BUS_GET_CONTIGUOUS: '/c_getn',
    RequestId.CONTROL_BUS_SET: '/c_set',
    RequestId.CONTROL_BUS_SET_CONTIGUOUS: '/c_setn',
    RequestId.DUMP_OSC: '/dumpOSC',
    RequestId.ERROR: '/error',
    RequestId.GROUP_DEEP_FREE: '/g_deepFree',
    RequestId.GROUP_DUMP_TREE: '/g_dumpTree',
    RequestId.GROUP_FREE_ALL: '/g_freeAll',
    RequestId.GROUP_HEAD: '/g_head',
    RequestId.GROUP_NEW: '/g_new',
    RequestId.GROUP_QUERY_TREE: '/g_queryTree',
    RequestId.GROUP_TAIL: '/g_tail',
    RequestId.NODE_AFTER: '/n_after',
    RequestId.NODE_BEFORE: '/n_before',
    RequestId.NODE_COMMAND: None,
    RequestId.NODE_FILL: '/n_fill',
    RequestId.NODE_FREE: '/n_free',
    RequestId.NODE_MAP_TO_AUDIO_BUS: '/n_mapa',
    RequestId.NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS: '/n_mapan',
    RequestId.NODE_MAP_TO_CONTROL_BUS: '/n_map',
    RequestId.NODE_MAP_TO_CONTROL_BUS_CONTIGUOUS: '/n_mapn',
    RequestId.NODE_ORDER: '/n_order',
    RequestId.NODE_QUERY: '/n_query',
    RequestId.NODE_RUN: '/n_run',
    RequestId.NODE_SET: '/n_set',
    RequestId.NODE_SET_CONTIGUOUS: '/n_setn',
    RequestId.NODE_TRACE: '/n_trace',
    RequestId.NOTHING: None,
    RequestId.NOTIFY: '/notify',
    RequestId.PARALLEL_GROUP_NEW: '/p_new',
    RequestId.QUIT: '/quit',
    RequestId.STATUS: '/status',
    RequestId.SYNC: '/sync',
    RequestId.SYNTHDEF_FREE: '/d_free',
    RequestId.SYNTHDEF_FREE_ALL: None,
    RequestId.SYNTHDEF_LOAD: '/d_load',
    RequestId.SYNTHDEF_LOAD_DIR: '/d_loadDir',
    RequestId.SYNTHDEF_RECEIVE: '/d_recv',
    RequestId.SYNTH_GET: '/s_get',
    RequestId.SYNTH_GET_CONTIGUOUS: '/s_getn',
    RequestId.SYNTH_NEW: '/s_new',
    RequestId.SYNTH_NEWARGS: None,
    RequestId.SYNTH_NOID: '/s_noid',
    RequestId.UGEN_COMMAND: '/u_cmd',
    }
