"""
Enumerations.
"""

from collections.abc import Sequence

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


class BinaryOperator(IntEnumeration):

    ### CLASS VARIABLES ###

    ABSOLUTE_DIFFERENCE = 38  # |a - b|
    ADDITION = 0
    AMCLIP = 40
    ATAN2 = 22
    BIT_AND = 14
    BIT_OR = 15
    BIT_XOR = 16
    CLIP2 = 42
    DIFFERENCE_OF_SQUARES = 34  # a*a - b*b
    EQUAL = 6
    EXCESS = 43
    EXPRANDRANGE = 48
    FLOAT_DIVISION = 4
    FILL = 29
    FIRST_ARG = 46
    FOLD2 = 44
    GREATEST_COMMON_DIVISOR = 18
    GREATER_THAN_OR_EQUAL = 11
    GREATER_THAN = 9
    HYPOT = 23
    HYPOTX = 24
    INTEGER_DIVISION = 3
    LEAST_COMMON_MULTIPLE = 17
    LESS_THAN_OR_EQUAL = 10
    LESS_THAN = 8
    MAXIMUM = 13
    MINIMUM = 12
    MODULO = 5
    MULTIPLICATION = 2
    NOT_EQUAL = 7
    POWER = 25
    RANDRANGE = 47
    RING1 = 30  # a * (b + 1) == a * b + a
    RING2 = 31  # a * b + a + b
    RING3 = 32  # a*a*b
    RING4 = 33  # a*a*b - a*b*b
    ROUND = 19
    ROUND_UP = 20
    SCALE_NEG = 41
    SHIFT_LEFT = 26
    SHIFT_RIGHT = 27
    SQUARE_OF_DIFFERENCE = 37  # (a - b)^2
    SQUARE_OF_SUM = 36  # (a + b)^2
    SUBTRACTION = 1
    SUM_OF_SQUARES = 35  # a*a + b*b
    THRESHOLD = 39
    TRUNCATION = 21
    UNSIGNED_SHIFT = 28
    WRAP2 = 45


class CalculationRate(IntEnumeration):
    """
    An enumeration of scsynth calculation-rates.

    ::

        >>> import supriya.synthdefs
        >>> supriya.CalculationRate.AUDIO
        CalculationRate.AUDIO

    ::

        >>> supriya.CalculationRate.from_expr("demand")
        CalculationRate.DEMAND

    """

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 1
    DEMAND = 3
    SCALAR = 0
    AR = 2
    KR = 1
    DR = 3
    IR = 0

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

            >>> supriya.CalculationRate.from_expr("demand")
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
        elif isinstance(expr, (supriya.synthdefs.OutputProxy, supriya.synthdefs.UGen)):
            return expr.calculation_rate
        elif isinstance(expr, supriya.synthdefs.Parameter):
            name = expr.parameter_rate.name
            if name == "TRIGGER":
                return CalculationRate.CONTROL
            return CalculationRate.from_expr(name)
        elif isinstance(expr, str):
            return super().from_expr(expr)
        elif isinstance(expr, Sequence):
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


class DoneAction(IntEnumeration):
    """
    An enumeration of ``scsynth`` UGen "done" actions.

    ::

        >>> import supriya.synthdefs
        >>> supriya.DoneAction(2)
        DoneAction.FREE_SYNTH

    ::

        >>> supriya.DoneAction.from_expr("pause synth")
        DoneAction.PAUSE_SYNTH

    """

    ### CLASS VARIABLES ###

    NOTHING = 0
    PAUSE_SYNTH = 1
    FREE_SYNTH = 2
    FREE_SYNTH_AND_PRECEDING_NODE = 3
    FREE_SYNTH_AND_FOLLOWING_NODE = 4
    FREE_SYNTH_AND_FREEALL_PRECEDING_NODE = 5
    FREE_SYNTH_AND_FREEALL_FOLLOWING_NODE = 6
    FREE_SYNTH_AND_ALL_PRECEDING_NODES_IN_GROUP = 7
    FREE_SYNTH_AND_ALL_FOLLOWING_NODES_IN_GROUP = 8
    FREE_SYNTH_AND_PAUSE_PRECEDING_NODE = 9
    FREE_SYNTH_AND_PAUSE_FOLLOWING_NODE = 10
    FREE_SYNTH_AND_DEEPFREE_PRECEDING_NODE = 11
    FREE_SYNTH_AND_DEEPFREE_FOLLOWING_NODE = 12
    FREE_SYNTH_AND_ALL_SIBLING_NODES = 13
    FREE_SYNTH_AND_ENCLOSING_GROUP = 14


class EnvelopeShape(IntEnumeration):

    ### CLASS VARIABLES ###

    CUBED = 7
    CUSTOM = 5
    EXPONENTIAL = 2
    LINEAR = 1
    SINE = 3
    SQUARED = 6
    STEP = 0
    WELCH = 4


class HeaderFormat(IntEnumeration):
    """
    An enumeration of soundfile header formats.

    ::

        >>> supriya.HeaderFormat.AIFF
        HeaderFormat.AIFF

    ::

        >>> supriya.HeaderFormat.from_expr("wav")
        HeaderFormat.WAV

    ::

        >>> header_format = supriya.HeaderFormat.from_expr("wav")
        >>> header_format.name.lower()
        'wav'

    """

    ### CLASS VARIABLES ###

    AIFF = 0
    IRCAM = 1
    NEXT = 2
    RAW = 3
    WAV = 4


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


class ParameterRate(IntEnumeration):
    """
    An enumeration of synthdef control rates.
    """

    ### CLASS VARIABLES ###

    AUDIO = 2
    CONTROL = 3
    SCALAR = 0
    TRIGGER = 1
    AR = 2
    KR = 3
    IR = 0
    TR = 1


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
    SYNTH_QUERY = 65
    UGEN_COMMAND = 20
    VERSION = 64

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
    SYNTH_QUERY = "/s_query"
    # SYNTH_NEWARGS = None
    SYNTH_NOID = "/s_noid"
    UGEN_COMMAND = "/u_cmd"
    VERSION = "/version"

    ### PUBLIC PROPERTIES ###

    @property
    def request_id(self):
        return RequestId.from_expr(self.name)


class SampleFormat(IntEnumeration):
    """
    An enumeration of soundfile sample formats.

    ::

        >>> supriya.SampleFormat.INT24
        SampleFormat.INT24

    ::

        >>> supriya.SampleFormat.from_expr("float")
        SampleFormat.FLOAT

    ::

        >>> sample_format = supriya.SampleFormat.INT24
        >>> sample_format.name.lower()
        'int24'

    """

    ### CLASS VARIABLES ###

    INT24 = 0
    ALAW = 1
    DOUBLE = 2
    FLOAT = 3
    INT8 = 4
    INT16 = 5
    INT32 = 6
    MULAW = 7


class SignalRange(IntEnumeration):
    """
    An enumeration of scsynth UGen signal ranges.

    ::

        >>> supriya.SignalRange.UNIPOLAR
        SignalRange.UNIPOLAR

    ::

        >>> supriya.SignalRange.from_expr("bipolar")
        SignalRange.BIPOLAR

    """

    ### CLASS VARIABLES ###

    UNIPOLAR = 0
    BIPOLAR = 1


class UnaryOperator(IntEnumeration):

    ### CLASS VARIABLES ###

    ABSOLUTE_VALUE = 5
    AMPLITUDE_TO_DB = 22
    ARCCOS = 32
    ARCSIN = 31
    ARCTAN = 33
    AS_FLOAT = 6
    AS_INT = 7
    BILINRAND = 40
    BIT_NOT = 4
    CEILING = 8
    COIN = 44
    COS = 29
    COSH = 35
    CUBED = 13
    DB_TO_AMPLITUDE = 21
    DIGIT_VALUE = 45
    DISTORT = 42
    EXPONENTIAL = 15
    FLOOR = 9
    FRACTIONAL_PART = 10
    HZ_TO_MIDI = 18
    HZ_TO_OCTAVE = 24
    HANNING_WINDOW = 49
    IS_NIL = 2
    LINRAND = 39
    LOG = 25
    LOG10 = 27
    LOG2 = 26
    MIDI_TO_HZ = 17
    SEMITONES_TO_RATIO = 19
    NEGATIVE = 0
    NOT = 1
    NOT_NIL = 3
    OCTAVE_TO_HZ = 23
    RAMP = 52
    RAND = 37
    RAND2 = 38
    RATIO_TO_SEMITONES = 20
    RECIPROCAL = 16
    RECTANGLE_WINDOW = 48
    S_CURVE = 53
    SIGN = 11
    SILENCE = 46
    SIN = 28
    SINH = 34
    SOFTCLIP = 43
    SQUARE_ROOT = 14
    SQUARED = 12
    SUM3RAND = 41
    TAN = 30
    TANH = 36
    THRU = 47
    TRIANGLE_WINDOW = 51
    WELCH_WINDOW = 50


class Unit(IntEnumeration):

    ### CLASS VARIABLES ###

    UNDEFINED = 0
    DECIBELS = 1
    AMPLITUDE = 2
    SECONDS = 3
    MILLISECONDS = 4
    HERTZ = 5
    SEMITONES = 6
