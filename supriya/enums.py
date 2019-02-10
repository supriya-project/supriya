import collections

from uqbar.enums import IntEnumeration, StrictEnumeration


class AddAction(IntEnumeration):
    """
    An enumeration of scsynth node add actions.
    """

    ### CLASS VARIABLES ###

    ADD_TO_HEAD = 0
    ADD_TO_TAIL = 1
    ADD_BEFORE = 2
    ADD_AFTER = 3
    REPLACE = 4


class CalculationRate(IntEnumeration):
    """
    An enumeration of scsynth calculation-rates.

    ::

        >>> import supriya.synthdefs
        >>> supriya.CalculationRate.AUDIO
        CalculationRate.AUDIO

    ::

        >>> supriya.CalculationRate.from_expr('demand')
        CalculationRate.DEMAND

    """

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 1
    DEMAND = 3
    SCALAR = 0

    ### PUBLIC METHODS ###

    @classmethod
    def from_expr(cls, expr):
        """
        Gets calculation-rate.

        ::

            >>> import supriya.synthdefs
            >>> import supriya.ugens

        ::

            >>> supriya.CalculationRate.from_expr(1)
            CalculationRate.SCALAR

        ::

            >>> supriya.CalculationRate.from_expr('demand')
            CalculationRate.DEMAND

        ::

            >>> collection = []
            >>> collection.append(supriya.ugens.DC.ar(0))
            >>> collection.append(supriya.ugens.DC.kr(1))
            >>> collection.append(2.0)
            >>> supriya.CalculationRate.from_expr(collection)
            CalculationRate.AUDIO

        ::
            >>> collection = []
            >>> collection.append(supriya.ugens.DC.kr(1))
            >>> collection.append(2.0)
            >>> supriya.CalculationRate.from_expr(collection)
            CalculationRate.CONTROL

        Return calculation-rate.
        """
        import supriya.synthdefs
        import supriya.ugens

        if isinstance(expr, (int, float)) and not isinstance(expr, cls):
            return CalculationRate.SCALAR
        elif isinstance(expr, (supriya.synthdefs.OutputProxy, supriya.ugens.UGen)):
            return expr.calculation_rate
        elif isinstance(expr, supriya.synthdefs.Parameter):
            name = expr.parameter_rate.name
            if name == "TRIGGER":
                return CalculationRate.CONTROL
            return CalculationRate.from_expr(name)
        elif isinstance(expr, str):
            return super().from_expr(expr)
        elif isinstance(expr, collections.Sequence):
            return max(CalculationRate.from_expr(item) for item in expr)
        elif hasattr(expr, "calculation_rate"):
            return cls.from_expr(expr.calculation_rate)
        return super().from_expr(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def token(self):
        if self == CalculationRate.SCALAR:
            return "ir"
        elif self == CalculationRate.CONTROL:
            return "kr"
        elif self == CalculationRate.AUDIO:
            return "ar"
        return "new"


class NodeAction(IntEnumeration):

    ### CLASS VARIABLES ###

    NODE_CREATED = 0
    NODE_REMOVED = 1
    NODE_ACTIVATED = 2
    NODE_DEACTIVATED = 3
    NODE_MOVED = 4
    NODE_QUERIED = 5

    ### PUBLIC METHODS ###

    @classmethod
    def from_address(cls, address):
        addresses = {
            "/n_end": cls.NODE_REMOVED,
            "/n_go": cls.NODE_CREATED,
            "/n_info": cls.NODE_QUERIED,
            "/n_move": cls.NODE_MOVED,
            "/n_off": cls.NODE_DEACTIVATED,
            "/n_on": cls.NODE_ACTIVATED,
        }
        action = addresses[address]
        return action


class RequestId(IntEnumeration):
    """
    An enumeration of scsynth request ids.
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
    def request_name(self):
        return RequestName.from_expr(self.name)


class RequestName(StrictEnumeration):
    """
    An enumeration of scsynth request names.
    """

    ### CLASS VARIABLES ###

    BUFFER_ALLOCATE = "/b_alloc"
    BUFFER_ALLOCATE_READ = "/b_allocRead"
    BUFFER_ALLOCATE_READ_CHANNEL = "/b_allocReadChannel"
    BUFFER_CLOSE = "/b_close"
    BUFFER_FILL = "/b_fill"
    BUFFER_FREE = "/b_free"
    BUFFER_GENERATE = "/b_gen"
    BUFFER_GET = "/b_get"
    BUFFER_GET_CONTIGUOUS = "/b_getn"
    BUFFER_QUERY = "/b_query"
    BUFFER_READ = "/b_read"
    BUFFER_READ_CHANNEL = "/b_readChannel"
    BUFFER_SET = "/b_set"
    BUFFER_SET_CONTIGUOUS = "/b_setn"
    BUFFER_WRITE = "/b_write"
    BUFFER_ZERO = "/b_zero"
    CLEAR_SCHEDULE = "/clearSched"
    COMMAND = "/cmd"
    CONTROL_BUS_FILL = "/c_fill"
    CONTROL_BUS_GET = "/c_get"
    CONTROL_BUS_GET_CONTIGUOUS = "/c_getn"
    CONTROL_BUS_SET = "/c_set"
    CONTROL_BUS_SET_CONTIGUOUS = "/c_setn"
    DUMP_OSC = "/dumpOSC"
    ERROR = "/error"
    GROUP_DEEP_FREE = "/g_deepFree"
    GROUP_DUMP_TREE = "/g_dumpTree"
    GROUP_FREE_ALL = "/g_freeAll"
    GROUP_HEAD = "/g_head"
    GROUP_NEW = "/g_new"
    GROUP_QUERY_TREE = "/g_queryTree"
    GROUP_TAIL = "/g_tail"
    NODE_AFTER = "/n_after"
    NODE_BEFORE = "/n_before"
    # NODE_COMMAND = None
    NODE_FILL = "/n_fill"
    NODE_FREE = "/n_free"
    NODE_MAP_TO_AUDIO_BUS = "/n_mapa"
    NODE_MAP_TO_AUDIO_BUS_CONTIGUOUS = "/n_mapan"
    NODE_MAP_TO_CONTROL_BUS = "/n_map"
    NODE_MAP_TO_CONTROL_BUS_CONTIGUOUS = "/n_mapn"
    NODE_ORDER = "/n_order"
    NODE_QUERY = "/n_query"
    NODE_RUN = "/n_run"
    NODE_SET = "/n_set"
    NODE_SET_CONTIGUOUS = "/n_setn"
    NODE_TRACE = "/n_trace"
    # NOTHING = None
    NOTIFY = "/notify"
    PARALLEL_GROUP_NEW = "/p_new"
    QUIT = "/quit"
    STATUS = "/status"
    SYNC = "/sync"
    SYNTHDEF_FREE = "/d_free"
    # SYNTHDEF_FREE_ALL = None
    SYNTHDEF_LOAD = "/d_load"
    SYNTHDEF_LOAD_DIR = "/d_loadDir"
    SYNTHDEF_RECEIVE = "/d_recv"
    SYNTH_GET = "/s_get"
    SYNTH_GET_CONTIGUOUS = "/s_getn"
    SYNTH_NEW = "/s_new"
    # SYNTH_NEWARGS = None
    SYNTH_NOID = "/s_noid"
    UGEN_COMMAND = "/u_cmd"

    ### PUBLIC PROPERTIES ###

    @property
    def request_id(self):
        return RequestId.from_expr(self.name)
