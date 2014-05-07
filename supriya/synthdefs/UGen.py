import collections
import enum


class UGen(object):
    r'''A UGen.
    '''

    ### CLASS VARIABLES ###

    class Rate(enum.IntEnum):
        AUDIO_RATE = 2
        CONTROL_RATE = 1
        SCALAR_RATE = 0

    __slots__ = (
        '_calculation_rate',
        '_inputs',
        '_special_index',
        )

    _argument_specifications = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        *args
        ):
        from supriya import synthdefs
        assert isinstance(calculation_rate, synthdefs.UGen.Rate)
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._special_index = special_index

    ### PRIVATE METHODS ###

    def add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index):
        self._inputs.append((ugen, output_index))

    @staticmethod
    def _compute_binary_rate(ugen_a, ugen_b):
        if ugen_a.calculation_rate == UGen.Rate.AUDIO_RATE:
            return UGen.RATE.AUDIO_RATE
        if hasattr(ugen_b, 'calculation_rate') and \
            ugen_b.calculation_rate == UGen.RAte.AUDIO_RATE:
            return UGen.Rate.AUDIO_RATE
        if ugen_a.calculation_rate == UGen.Rate.CONTROL_RATE:
            return UGen.Rate.CONTROL_RATE
        if hasattr(ugen_b, 'calculation_rate') and \
            ugen_b.calculation_rate == UGen.Rate.CONTROL_RATE:
            return UGen.Rate.CONTROL_RATE
        return UGen.Rate.SCALAR_RATE

    @staticmethod
    def _expand_multichannel(arguments):
        r'''Expands ugens into multichannel arrays.

        ::

            >>> import supriya
            >>> arguments = (0, [1, 2], [3, 4, 5])
            >>> supriya.synthdefs.UGen._expand_multichannel(arguments)
            [[0, 1, 3], [0, 2, 4], [0, 1, 5]]

        '''
        maximum_length = 1
        for argument in arguments:
            if isinstance(argument, collections.Sequence):
                maximum_length = max(maximum_length, len(argument))
        result = []
        for i in range(maximum_length):
            result.append([])
            for argument in arguments:
                if isinstance(argument, collections.Sequence):
                    result[i].append(argument[i % len(argument)])
                else:
                    result[i].append(argument)
        return result

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate]

    @classmethod
    def _new(cls, calculation_rate, special_index, *args):
        from supriya import synthdefs
        assert isinstance(calculation_rate, UGen.Rate)
        argument_lists = UGen._expand_multichannel(args)
        ugens = []
        for argument_list in argument_lists:
            ugen = cls(
                calculation_rate=calculation_rate,
                special_index=special_index,
                )
            for i in range(len(cls.argument_specifications)):
                argument_specification = cls.argument_specifications[i]
                if i < len(argument_list):
                    argument = argument_list[i]
                else:
                    argument = None
                argument_specification.configure(ugen, argument)
            ugens.append(ugens)
        if len(ugens) == 1:
            return ugens[0]
        return synthdefs.UGenArray(ugens)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        from supriya import ugens
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = ugens.BinaryOpUGen.BinaryOperator.PLUS
        return ugens.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __div__(self, expr):
        from supriya import ugens
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = ugens.BinaryOpUGen.BinaryOperator.DIVIDE
        return ugens.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __mod__(self, expr):
        from supriya import ugens
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = ugens.BinaryOpUGen.BinaryOperator.MOD,
        return ugens.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __mul__(self, expr):
        from supriya import ugens
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = ugens.BinaryOpUGen.BinaryOperator.TIMES
        return ugens.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __neg__(self):
        from supriya import ugens
        calculation_rate = self.calculation_rate
        special_index = ugens.UnaryOpUGen.UnaryOperator.NEG
        return ugens.UnaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            )

    def __sub__(self, expr):
        from supriya import ugens
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = ugens.BinaryOpUGen.BinaryOperator.MINUS
        return ugens.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, *args):
        ugen = cls._new(
            UGen.Rate.AUDIO_RATE,
            cls.special_index,
            *args
            )
        return ugen

    def compile(self, synthdef):
        def compileInput(i, synthdef):
            result = []
            if type(i) == float:
                result.append(SynthDef._encode_unsigned_int_16bit(0xffff))
                constant_index = synthdef._get_constant_index(i)
                result.append(SynthDef._encode_unsigned_int_16bit(
                    constant_index))
            else:
                ugen_lookup = synthdef._get_ugen_index(i[0])
                result.append(SynthDef._encode_unsigned_int_16bit(
                    ugen_lookup[0]))
                result.append(SynthDef._encode_unsigned_int_16bit(
                    ugen_lookup[1]))
            return ''.join(result)
        from supriya.synthdefs import SynthDef
        outputs = self._get_outputs()
        result = []
        result.append(SynthDef._encode_string(self.classname))
        result.append(SynthDef._encode_unsigned_int_8bit(self.calcrate))
        result.append(SynthDef._encode_unsigned_int_16bit(len(self.inputs)))
        result.append(SynthDef._encode_unsigned_int_16bit(len(outputs)))
        result.append(SynthDef._encode_unsigned_int_16bit(self.special_index))
        for i in self.inputs:
            result.append(self.compileInput(i, synthdef))
        for o in outputs:
            result.append(SynthDef._encode_unsigned_int_8bit(o))
        return result

    @classmethod
    def kr(cls, *args):
        ugen = cls._new(
            UGen.Rate.CONTROL_RATE,
            cls.special_index,
            *args
            )
        return ugen
