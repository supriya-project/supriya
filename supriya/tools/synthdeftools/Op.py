# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Op(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = ()

    ### PUBLIC METHODS ###

    '''
    # ABSOLUTE_VALUE = 5
    # AMPLITUDE_TO_DB = 22
    ARCCOS = 32
    ARCSIN = 31
    ARCTAN = 33
    AS_FLOAT = 6
    AS_INT = 7
    BILINRAND = 40
    BIT_NOT = 4
    # CEILING = 8
    COIN = 44
    COS = 29
    COSH = 35
    CUBED = 13
    # DB_TO_AMPLITUDE = 21
    DIGIT_VALUE = 45
    # DISTORT = 42
    # EXPONENTIAL = 15
    # FLOOR = 9
    # FRACTIONAL_PART = 10
    # HZ_TO_MIDI = 18
    # HZ_TO_OCTAVE = 24
    # HANNING_WINDOW = 49
    IS_NIL = 2
    LINRAND = 39
    # LOG = 25
    # LOG10 = 27
    # LOG2 = 26
    # MIDI_TO_HZ = 17
    # SEMITONES_TO_RATIO = 19
    # NEGATIVE = 0
    NOT = 1
    NOT_NIL = 3
    # OCTAVE_TO_HZ = 23
    RAMP = 52
    RAND = 37
    RAND2 = 38
    # RATIO_TO_SEMITONES = 20
    # RECIPROCAL = 16
    # RECTANGLE_WINDOW = 48
    S_CURVE = 53
    # SIGN = 11
    SILENCE = 46
    SIN = 28
    SINH = 34
    # SOFTCLIP = 43
    # SQUARE_ROOT = 14
    # SQUARED = 12
    SUM3RAND = 41
    TAN = 30
    # TANH = 36
    THRU = 47
    # TRIANGLE_WINDOW = 51
    # WELCH_WINDOW = 50
    '''

    '''
    # ABSOLUTE_DIFFERENCE = 38  # |a - b|
    # ADDITION = 0
    AMCLIP = 40
    ATAN2 = 22
    BIT_AND = 14
    BIT_OR = 15
    BIT_XOR = 16
    CLIP2 = 42
    DIFFERENCE_OF_SQUARES = 34  # a*a - b*b
    # EQUAL = 6
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
    # MAXIMUM = 13
    # MINIMUM = 12
    # MODULO = 5
    # MULTIPLICATION = 2
    # NOT_EQUAL = 7
    # POWER = 25
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
    # SUBTRACTION = 1
    SUM_OF_SQUARES = 35  # a*a + b*b
    THRESHOLD = 39
    TRUNCATION = 21
    UNSIGNED_SHIFT = 28
    WRAP2 = 45
    '''

    @staticmethod
    def absolute_difference(left, right):
        r'''Calculates absolute difference between `left` and `right`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = Op.absolute_difference(left, right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:ABSOLUTE_DIFFERENCE[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:ABSOLUTE_DIFFERENCE[1:right]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.ABSOLUTE_DIFFERENCE,
            )

    @staticmethod
    def absolute_value(source):
        r'''Calculates absolute value of `source`.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.absolute_value(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:ABSOLUTE_VALUE[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.ABSOLUTE_VALUE,
            )

    @staticmethod
    def amplitude_to_db(source):
        r'''Converts `source` from amplitude to decibels.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.amplitude_to_db(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:AMPLITUDE_TO_DB[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.AMPLITUDE_TO_DB,
            )

    @staticmethod
    def as_hanning_window(source):
        r'''Calculates Hanning window value at `source`.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.as_hanning_window(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:HANNING_WINDOW[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.HANNING_WINDOW,
            )

    @staticmethod
    def as_rectangle_window(source):
        r'''Calculates rectangle window value at `source`.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.as_rectangle_window(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:RECTANGLE_WINDOW[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.RECTANGLE_WINDOW,
            )

    @staticmethod
    def as_s_curve(source):
        r'''Calculates S-curve value at `source`.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.as_s_curve(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:S_CURVE[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.S_CURVE,
            )

    @staticmethod
    def as_triangle_window(source):
        r'''Calculates triangle window value at `source`.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.as_triangle_window(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:TRIANGLE_WINDOW[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.TRIANGLE_WINDOW,
            )

    @staticmethod
    def as_welch_window(source):
        r'''Calculates Welch window value at `source`.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.as_welch_window(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:WELCH_WINDOW[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.WELCH_WINDOW,
            )

    @staticmethod
    def ceiling(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.CEILING,
            )

    @staticmethod
    def cubed(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.CUBED,
            )

    @staticmethod
    def db_to_amplitude(source):
        r'''Converts `source` from decibels to amplitude.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.db_to_amplitude(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:DB_TO_AMPLITUDE[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.DB_TO_AMPLITUDE,
            )

    @staticmethod
    def distort(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.DISTORT,
            )

    @staticmethod
    def exponential(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.EXPONENTIAL,
            )

    @staticmethod
    def floor(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.FLOOR,
            )

    @staticmethod
    def fractional_part(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.FRACTIONAL_PART,
            )

    @staticmethod
    def hz_to_midi(source):
        r'''Converts `source` from Hertz to midi note number.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.hz_to_midi(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:HZ_TO_MIDI[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.HZ_TO_MIDI,
            )

    @staticmethod
    def hz_to_octave(source):
        r'''Converts `source` from Hertz to octave number.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.hz_to_octave(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:HZ_TO_OCTAVE[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.HZ_TO_OCTAVE,
            )

    @staticmethod
    def is_equal(left, right):
        r'''Calculates equality between `left` and `right`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = Op.is_equal(left, right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:EQUAL[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:EQUAL[1:right]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.EQUAL,
            )

    @staticmethod
    def is_not_equal(left, right):
        r'''Calculates inequality between `left` and `right`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = Op.is_not_equal(left, right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:NOT_EQUAL[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:NOT_EQUAL[1:right]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.NOT_EQUAL,
            )

    @staticmethod
    def log(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.LOG,
            )

    @staticmethod
    def log2(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.LOG2,
            )

    @staticmethod
    def log10(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.LOG10,
            )

    @staticmethod
    def maximum(left, right):
        r'''Calculates maximum between `left` and `right`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = Op.maximum(left, right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:MAXIMUM[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:MAXIMUM[1:right]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.MAXIMUM,
            )

    @staticmethod
    def midi_to_hz(source):
        r'''Converts `source` from midi note number to Hertz.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.midi_to_hz(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:MIDI_TO_HZ[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.MIDI_TO_HZ,
            )

    @staticmethod
    def minimum(left, right):
        r'''Calculates minimum between `left` and `right`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = Op.minimum(left, right)
            >>> print(operation)
            SynthDef f80c0a7b300911e9eff0e8760f5fab18 {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:MINIMUM[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:MINIMUM[1:right]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.MINIMUM,
            )

    @staticmethod
    def octave_to_hz(source):
        r'''Converts `source` from octave number to Hertz.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.octave_to_hz(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:OCTAVE_TO_HZ[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.OCTAVE_TO_HZ,
            )

    @staticmethod
    def power(left, right):
        r'''Calculates `left` raised to the power of `right`.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> operation = Op.power(left, right)
            >>> print(operation)
            SynthDef ... {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:POWER[0:left]
                1_WhiteNoise[0] -> 2_BinaryOpUGen:POWER[1:right]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.POWER,
            )

    @staticmethod
    def ratio_to_semitones(source):
        r'''Converts `source` from frequency ratio to semitone distance.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.ratio_to_semitones(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:RATIO_TO_SEMITONES[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.RATIO_TO_SEMITONES,
            )

    @staticmethod
    def reciprocal(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.RECIPROCAL,
            )

    @staticmethod
    def semitones_to_ratio(source):
        r'''Converts `source` from semitone distance to frequency ratio.

        ::

            >>> source = ugentools.DC.ar(source=0.5)
            >>> operation = Op.semitones_to_ratio(source)
            >>> print(operation)
            SynthDef ... {
                const_0:0.5 -> 0_DC[0:source]
                0_DC[0] -> 1_UnaryOpUGen:SEMITONES_TO_RATIO[0:source]
            }

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.SEMITONES_TO_RATIO,
            )

    @staticmethod
    def sign(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.SIGN,
            )

    @staticmethod
    def softclip(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.SOFTCLIP,
            )

    @staticmethod
    def square_root(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.SQUARE_ROOT,
            )

    @staticmethod
    def squared(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.SQUARED,
            )

    @staticmethod
    def tanh(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.TANH,
            )