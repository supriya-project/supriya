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
        **kwargs
        ):
        from supriya import synthdefs
        assert isinstance(calculation_rate, synthdefs.UGen.Rate), calculation_rate
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._special_index = special_index

    ### PRIVATE METHODS ###

    def _add_constant_input(self, value):
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
            >>> arguments = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = supriya.synthdefs.UGen._expand_multichannel(arguments)
            >>> for x in result:
            ...     x
            ...
            {'bar': 1, 'foo': 0, 'baz': 3}
            {'bar': 2, 'foo': 0, 'baz': 4}
            {'bar': 1, 'foo': 0, 'baz': 5}

        '''
        maximum_length = 1
        result = []
        for name, value in arguments.items():
            if isinstance(value, collections.Sequence):
                maximum_length = max(maximum_length, len(value))
        for i in range(maximum_length):
            result.append({})
            for name, value in arguments.items():
                if isinstance(value, collections.Sequence):
                    result[i][name] = value[i % len(value)]
                else:
                    result[i][name] = value
        return result

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate]

    def _get_ugen(self):
        return self

    @classmethod
    def _new(cls, calculation_rate, special_index, **kwargs):
        from supriya import synthdefs
        assert isinstance(calculation_rate, UGen.Rate)
        argument_dicts = UGen._expand_multichannel(kwargs)
        ugens = []
        for argument_dict in argument_dicts:
            ugen = cls(
                calculation_rate=calculation_rate,
                special_index=special_index,
                **argument_dict
                )
#            for i in range(len(cls._argument_specifications)):
#                argument_specification = cls._argument_specifications[i]
#                if i < len(argument_list):
#                    argument = argument_list[i]
#                else:
#                    argument = None
#                argument_specification.configure(ugen, argument)
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdefs.UGenArray(ugens)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.PLUS
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __div__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.DIVIDE
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __mod__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.MOD,
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __mul__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.TIMES
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    def __neg__(self):
        from supriya import synthdefs
        calculation_rate = self.calculation_rate
        special_index = synthdefs.UnaryOpUGen.UnaryOperator.NEG
        return synthdefs.UnaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            )

    def __sub__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.MINUS
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            self,
            expr,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, **kwargs):
        ugen = cls._new(
            UGen.Rate.AUDIO_RATE,
            cls.special_index,
            **kwargs
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
    def kr(cls, **kwargs):
        ugen = cls._new(
            UGen.Rate.CONTROL_RATE,
            cls.special_index,
            **kwargs
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def special_index(self):
        return self._special_index
