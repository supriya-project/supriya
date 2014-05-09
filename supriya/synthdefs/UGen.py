from __future__ import print_function
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
        '_antecedents',
        '_calculation_rate',
        '_decendants',
        '_inputs',
        '_special_index',
        '_synthdef',
        '_width_first_antecedents',
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
        for i in range(len(self._argument_specifications)):
            argument_specification = self._argument_specifications[i]
            argument_name = argument_specification.name
            argument_value = kwargs.get(argument_name, None)
            prototype = (
                type(None),
                float,
                int,
                UGen,
                synthdefs.OutputProxy,
                )
            assert isinstance(argument_value, prototype), argument_value
            argument_specification.configure(self, argument_value)
        self._antecedents = []
        self._decendants = []
        self._synthdef = None
        self._width_first_antecedents = []

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.PLUS.value
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            left=self,
            right=expr,
            )

    def __div__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.DIVIDE.value
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            left=self,
            right=expr,
            )

    def __mod__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.MOD.value
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            left=self,
            right=expr,
            )

    def __mul__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.TIMES.value
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            left=self,
            right=expr,
            )

    def __neg__(self):
        from supriya import synthdefs
        calculation_rate = self.calculation_rate
        special_index = synthdefs.UnaryOpUGen.UnaryOperator.NEG.value
        return synthdefs.UnaryOpUGen._new(
            calculation_rate,
            special_index,
            source=self,
            )

    def __sub__(self, expr):
        from supriya import synthdefs
        calculation_rate = self._compute_binary_rate(self, expr)
        special_index = synthdefs.BinaryOpUGen.BinaryOperator.MINUS.value
        return synthdefs.BinaryOpUGen._new(
            calculation_rate,
            special_index,
            left=self,
            right=expr,
            )

    ### PRIVATE METHODS ###

    def _add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index):
        from supriya import synthdefs
        output_proxy = synthdefs.OutputProxy(
            output_index=output_index,
            source=ugen,
            )
        self._inputs.append(output_proxy)

    @staticmethod
    def _compute_binary_rate(ugen_a, ugen_b):
        if ugen_a.calculation_rate == UGen.Rate.AUDIO_RATE:
            return UGen.Rate.AUDIO_RATE
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
                    value = value[i % len(value)]
                    result[i][name] = value
                else:
                    result[i][name] = value
        return result

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate]

    def _get_ugen(self):
        return self

    def _initialize_topological_sort(self):
        from supriya import synthdefs
        for input_ in self.inputs:
            if isinstance(input_, synthdefs.OutputProxy):
                ugen = input_.source
                if ugen not in self.antecedents:
                    self.antecedents.append(ugen)
                if self not in ugen.descendants:
                    ugen.descendants.append(self)
        for ugen in self.width_first_antecedents:
            if ugen not in self.antecedents:
                self.antecedents.append(ugen)
            if self not in ugen.descendants:
                ugen.descendants.append(self)

    def _make_available(self, synthdef):
        if not self.antecedents:
            if self not in self.synthdef.available_ugens:
                self.synthdef.available_ugens.append(self)

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
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdefs.UGenArray(ugens)

    def _optimize_graph(self):
        pass

    def _remove_antecedent(self, ugen):
        self.antecedents.remove(ugen)
        self._make_available()

    def _schedule(self, out_stack):
        for ugen in reversed(self.descendants):
            ugen._remove_antecedent(self)
        out_stack.append(self)

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, **kwargs):
        ugen = cls._new(
            calculation_rate=UGen.Rate.AUDIO_RATE,
            special_index=0,
            **kwargs
            )
        return ugen

    def compile(self, synthdef):
        def compile_input_spec(i, synthdef):
            from supriya import synthdefs
            result = []
            if isinstance(i, float):
                result.append(SynthDef._encode_unsigned_int_32bit(0xffffffff))
                constant_index = synthdef._get_constant_index(i)
                result.append(SynthDef._encode_unsigned_int_32bit(
                    constant_index))
            elif isinstance(i, synthdefs.OutputProxy):
                ugen = i.source
                output_index = i.output_index
                ugen_index = synthdef._get_ugen_index(ugen)
                result.append(SynthDef._encode_unsigned_int_32bit(ugen_index))
                result.append(SynthDef._encode_unsigned_int_32bit(output_index))
            else:
                raise Exception('Unhandled input spec: {}'.format(i))
            return ''.join(result)
        from supriya.synthdefs import SynthDef
        outputs = self._get_outputs()
        result = []
        result.append(SynthDef._encode_string(type(self).__name__))
        result.append(SynthDef._encode_unsigned_int_8bit(self.calculation_rate))
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.inputs)))
        result.append(SynthDef._encode_unsigned_int_32bit(len(outputs)))
        result.append(SynthDef._encode_unsigned_int_16bit(int(self.special_index)))
        for i in self.inputs:
            result.append(compile_input_spec(i, synthdef))
        for o in outputs:
            result.append(SynthDef._encode_unsigned_int_8bit(o))
        result = ''.join(result)
        return result

    @classmethod
    def kr(cls, **kwargs):
        ugen = cls._new(
            calculation_rate=UGen.Rate.CONTROL_RATE,
            special_index=0,
            **kwargs
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def antecedents(self):
        return self._antecedents

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def descendants(self):
        return self._descendants

    @property
    def inputs(self):
        return tuple(self._inputs)

    @property
    def special_index(self):
        return self._special_index

    @property
    def synthdef(self):
        return self._synthdef

    @synthdef.setter
    def synthdef(self, synthdef):
        from supriya import synthdefs
        assert isinstance(synthdef, synthdefs.SynthDef)
        self._synthdef = synthdef

    @property
    def width_first_antecedents(self):
        return self._width_first_antecedents
