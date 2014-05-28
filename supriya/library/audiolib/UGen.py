# -*- encoding: utf-8 -*-

from __future__ import print_function
import abc
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
        TRIGGER_RATE = -1

    class SignalRange(enum.IntEnum):
        UNIPOLAR = 0
        BIPOLAR = 1

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_antecedents',
        '_calculation_rate',
        '_descendants',
        '_inputs',
        '_output_proxies',
        '_special_index',
        '_synthdef',
        '_width_first_antecedents',
        )

    _argument_specifications = ()

    _unexpanded_argument_names = None

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        **kwargs
        ):
        from supriya import audiolib
        assert isinstance(calculation_rate, audiolib.UGen.Rate), calculation_rate
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._special_index = special_index
        for i in range(len(self._argument_specifications)):
            argument_specification = self._argument_specifications[i]
            argument_name = argument_specification.name
            argument_value = kwargs.get(argument_name, None)
            argument_value = None
            if argument_name in kwargs:
                argument_value = kwargs[argument_name]
                del(kwargs[argument_name])
            prototype = (
                type(None),
                float,
                int,
                UGen,
                audiolib.OutputProxy,
                )
            assert isinstance(argument_value, prototype), argument_value
            argument_specification.configure(self, argument_value)
        if kwargs:
            raise ValueError(kwargs)
        self._antecedents = []
        self._descendants = []
        self._output_proxies = tuple(
            audiolib.OutputProxy(self, i)
            for i in range(len(self))
            )
        self._synthdef = None
        self._width_first_antecedents = []

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        return self._compute_binary_op(expr, 'ADD')

    def __div__(self, expr):
        return self._compute_binary_op(expr, 'FDIV')

    def __getattr__(self, attr):
        try:
            object.__getattr__(self, attr)
        except AttributeError:
            for i, argument_specification in enumerate(
                self._argument_specifications):
                if argument_specification.name == attr:
                    return self.inputs[i]
        raise AttributeError

    def __getitem__(self, i):
        return self._output_proxies[i]

    def __len__(self):
        return 1

    def __mod__(self, expr):
        return self._compute_binary_op(expr, 'MOD')

    def __mul__(self, expr):
        return self._compute_binary_op(expr, 'MUL')

    def __neg__(self):
        return self._compute_unary_op('NEG')

    def __radd__(self, expr):
        return self.__add__(expr)

    def __rdiv__(self, expr):
        return self.__div__(expr)

    def __repr__(self):
        calculation_abbreviations = {
            self.Rate.AUDIO_RATE: 'ar',
            self.Rate.CONTROL_RATE: 'kr',
            self.Rate.SCALAR_RATE: 'ir',
            self.Rate.TRIGGER_RATE: 'tr',
            }
        string = '{}.{}()'.format(
            type(self).__name__,
            calculation_abbreviations[self.calculation_rate]
            )
        return string

    def __rmul__(self, expr):
        return self.__mul__(expr)

    def __rsub__(self, expr):
        return self.__sub__(expr)

    def __sub__(self, expr):
        return self._compute_binary_op(expr, 'SUB')

    ### PRIVATE METHODS ###

    def _add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index=None):
        from supriya import audiolib
        if isinstance(ugen, audiolib.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = audiolib.OutputProxy(
                output_index=output_index,
                source=ugen,
                )
        self._inputs.append(output_proxy)

    def _collect_constants(self):
        from supriya import audiolib
        for input_ in self._inputs:
            if not isinstance(input_, audiolib.OutputProxy):
                self.synthdef._add_constant(float(input_))

    def _compute_binary_op(self, expr, op_name):
        from supriya import audiolib
        calculation_rate = self._compute_binary_rate(self, expr)
        operator = audiolib.BinaryOpUGen.BinaryOperator[op_name]
        special_index = operator.value
        return audiolib.BinaryOpUGen._new(
            calculation_rate=calculation_rate,
            left=self,
            right=expr,
            special_index=special_index,
            )

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

    def _compute_unary_op(self, op_name):
        from supriya import audiolib
        operator = audiolib.UnaryOpUGen.UnaryOperator[op_name]
        special_index = operator.value
        return audiolib.UnaryOpUGen._new(
            calculation_rate=self.calculation_rate,
            source=self,
            special_index=special_index,
            )

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate]

    def _get_source(self):
        return self

    def _initialize_topological_sort(self):
        from supriya import audiolib
        for input_ in self.inputs:
            if isinstance(input_, audiolib.OutputProxy):
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

    def _make_available(self):
        if not self.antecedents:
            if self not in self.synthdef._available_ugens:
                self.synthdef._available_ugens.append(self)

    @classmethod
    def _new(cls, calculation_rate, special_index, **kwargs):
        import sys
        from supriya import audiolib
        if sys.version_info[0] == 2:
            import funcsigs
            get_signature = funcsigs.signature
        else:
            import inspect
            get_signature = inspect.signature
        assert isinstance(calculation_rate, UGen.Rate)
        argument_dicts = UGen.expand_arguments(
            kwargs, unexpanded_argument_names=cls._unexpanded_argument_names)
        ugens = []
        signature = get_signature(cls.__init__)
        has_custom_special_index = 'special_index' in signature.parameters
        for argument_dict in argument_dicts:
            if has_custom_special_index:
                ugen = cls(
                    calculation_rate=calculation_rate,
                    special_index=special_index,
                    **argument_dict
                    )
            else:
                ugen = cls(
                    calculation_rate=calculation_rate,
                    **argument_dict
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return audiolib.UGenArray(ugens)

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
            from supriya import audiolib
            result = []
            if isinstance(i, float):
                result.append(SynthDef._encode_unsigned_int_32bit(0xffffffff))
                constant_index = synthdef._get_constant_index(i)
                result.append(SynthDef._encode_unsigned_int_32bit(
                    constant_index))
            elif isinstance(i, audiolib.OutputProxy):
                ugen = i.source
                output_index = i.output_index
                ugen_index = synthdef._get_ugen_index(ugen)
                result.append(SynthDef._encode_unsigned_int_32bit(ugen_index))
                result.append(SynthDef._encode_unsigned_int_32bit(output_index))
            else:
                raise Exception('Unhandled input spec: {}'.format(i))
            return bytearray().join(result)
        from supriya.library.audiolib import SynthDef
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
        result = bytearray().join(result)
        return result

    @staticmethod
    def expand_arguments(arguments, unexpanded_argument_names=None):
        r'''Expands ugens into multichannel arrays.

        ::

            >>> import supriya
            >>> arguments = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = supriya.audiolib.UGen.expand_arguments(arguments)
            >>> for x in result:
            ...     x
            ...
            {'bar': 1, 'foo': 0, 'baz': 3}
            {'bar': 2, 'foo': 0, 'baz': 4}
            {'bar': 1, 'foo': 0, 'baz': 5}

        ::

            >>> arguments = {'bus': (8, 9), 'source': (1, 2, 3)}
            >>> result = supriya.audiolib.UGen.expand_arguments(
            ...     arguments,
            ...     unexpanded_argument_names=('source',),
            ...     )
            >>> for x in result:
            ...     x
            ...
            {'bus': 8, 'source': (1, 2, 3)}
            {'bus': 9, 'source': (1, 2, 3)}

        '''
        cached_unexpanded_arguments = {}
        if unexpanded_argument_names is not None:
            for argument_name in unexpanded_argument_names:
                if argument_name not in arguments:
                    continue
                cached_unexpanded_arguments[argument_name] = \
                    arguments[argument_name]
                del(arguments[argument_name])
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
        for expanded_arguments in result:
            expanded_arguments.update(cached_unexpanded_arguments)
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
    def signal_range(self):
        return self.SignalRange.BIPOLAR

    @property
    def special_index(self):
        return self._special_index

    @property
    def synthdef(self):
        return self._synthdef

    @synthdef.setter
    def synthdef(self, synthdef):
        from supriya import audiolib
        assert isinstance(synthdef, audiolib.SynthDef)
        self._synthdef = synthdef

    @property
    def width_first_antecedents(self):
        return self._width_first_antecedents
