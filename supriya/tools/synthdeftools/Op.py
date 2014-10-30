# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Op(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = ()

    ### PUBLIC METHODS ###

    @staticmethod
    def absolute_difference(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.ABSOLUTE_DIFFERENCE,
            )

    @staticmethod
    def amplitude_to_db(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.AMPLITUDE_TO_DB,
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
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.HZ_TO_MIDI,
            )

    @staticmethod
    def hz_to_octave(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.HZ_TO_OCTAVE,
            )

    @staticmethod
    def is_equal_to(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.EQUAL,
            )

    @staticmethod
    def is_not_equal_to(left, right):
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
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.MAX,
            )

    @staticmethod
    def midi_to_hz(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.MIDI_TO_HZ,
            )

    @staticmethod
    def minimum(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.MIN,
            )

    @staticmethod
    def octave_to_hz(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            synthdeftools.UnaryOperator.OCTAVE_TO_HZ,
            )

    @staticmethod
    def pow(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            synthdeftools.BinaryOperator.POW,
            )

    @staticmethod
    def ratio_to_semitones(source):
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