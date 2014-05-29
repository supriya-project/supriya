import enum
from supriya.library.audiolib.Argument import Argument
from supriya.library.audiolib.UGen import UGen


class UnaryOpUGen(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        )

    class UnaryOperator(enum.IntEnum):
        NEG = 0
        NOT = 1
        IS_NIL = 2
        NOT_NIL = 3
        BIT_NOT = 4
        ABS = 5
        AS_FLOAT = 6
        AS_INT = 7
        CEIL = 8
        FLOOR = 9
        FRACTION = 10
        SIGN = 11
        SQUARED = 12
        CUBED = 13
        SQRT = 14
        EXP = 15
        RECIPROCAL = 16
        MIDI_TO_FREQ = 17
        FREQ_TO_MIDI = 18
        MIDI_TO_RATIO = 19
        RATIO_TO_MIDI = 20
        DB_TO_AMP = 21
        AMP_TO_DB = 22
        OCTAVE_TO_FREQ = 23
        FREQ_TO_OCTAVE = 24
        LOG = 25
        LOG2 = 26
        LOG10 = 27
        SIN = 28
        COS = 29
        TAN = 30
        ARCSIN = 31
        ARCCOS = 32
        ARCTAN = 33
        SINH = 34
        COSH = 35
        TANH = 36
        RAND = 37
        RAND2 = 38
        LINRAND = 39
        BILINRAND = 40
        SUM3RAND = 41
        DISTORT = 42
        SOFTCLIP = 43
        COIN = 44
        DIGIT_VALUE = 45
        SILENCE = 46
        THRU = 47
        RECTANGLE_WINDOW = 48
        HANNING_WINDOW = 49
        WELCH_WINDOW = 50
        TRIANGLE_WINDOW = 51
        RAMP = 52
        SCURVE = 53

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            special_index=special_index,
            )
