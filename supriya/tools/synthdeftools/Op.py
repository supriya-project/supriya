# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Op(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    @staticmethod
    def absolute_difference(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            'absdiff',
            )

    @staticmethod
    def amplitude_to_db(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'amplitude_to_db',
            )

    @staticmethod
    def ceiling(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'ceiling',
            )

    @staticmethod
    def cubed(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'cubed',
            )

    @staticmethod
    def db_to_amplitude(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'db_to_amplitude',
            )

    @staticmethod
    def exponential(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'exponential',
            )

    @staticmethod
    def floor(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'floor',
            )

    @staticmethod
    def fractional_part(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'fractional_part',
            )

    @staticmethod
    def hz_to_midi(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'hz_to_midi',
            )

    @staticmethod
    def hz_to_octave(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'hz_to_octave',
            )

    @staticmethod
    def is_equal_to(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            'eq',
            )

    @staticmethod
    def is_not_equal_to(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            'ne',
            )

    @staticmethod
    def log(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'log',
            )

    @staticmethod
    def log2(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'log2',
            )

    @staticmethod
    def log10(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'log10',
            )

    @staticmethod
    def maximum(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            'max',
            )

    @staticmethod
    def midi_to_hz(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'midi_to_hz',
            )

    @staticmethod
    def minimum(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            'min',
            )

    @staticmethod
    def octave_to_hz(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'octave_to_hz',
            )

    @staticmethod
    def pow(left, right):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_binary_op(
            left,
            right,
            'pow',
            )

    @staticmethod
    def ratio_to_semitones(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'ratio_to_semitones',
            )

    @staticmethod
    def reciprocal(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'reciprocal',
            )

    @staticmethod
    def semitones_to_ratio(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'semitones_to_ratio',
            )

    @staticmethod
    def sign(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'sign',
            )

    @staticmethod
    def softclip(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'softclip',
            )

    @staticmethod
    def square_root(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'square_root',
            )

    @staticmethod
    def squared(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'squared',
            )

    @staticmethod
    def tanh(source):
        from supriya import synthdeftools
        return synthdeftools.UGenMethodMixin._compute_unary_op(
            source,
            'tanh',
            )
