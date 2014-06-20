# -*- encoding: utf-8 -*-
from __future__ import print_function
import abc
import collections
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class UGen(UGenMethodMixin):
    r'''A UGen.
    '''

    ### CLASS VARIABLES ###

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

    _ordered_input_names = ()

    _unexpanded_input_names = None

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        calculation_rate=None,
        special_index=0,
        **kwargs
        ):
        from supriya import synthdeftools
        assert isinstance(calculation_rate, synthdeftools.CalculationRate), \
            calculation_rate
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._special_index = special_index
        for i in range(len(self._ordered_input_names)):
            input_name = self._ordered_input_names[i]
            input_value = kwargs.get(input_name, None)
            if input_name in kwargs:
                input_value = kwargs[input_name]
                del(kwargs[input_name])
            prototype = (
                type(None),
                float,
                int,
                UGen,
                synthdeftools.OutputProxy,
                )
            if self._unexpanded_input_names and \
                input_name in self._unexpanded_input_names:
                prototype += (tuple,)
            assert isinstance(input_value, prototype), input_value
            self._configure_input(input_name, input_value)
        if kwargs:
            raise ValueError(kwargs)
        self._validate_inputs()
        self._antecedents = []
        self._descendants = []
        self._output_proxies = tuple(
            synthdeftools.OutputProxy(self, i)
            for i in range(len(self))
            )
        self._synthdef = None
        self._width_first_antecedents = []

    ### SPECIAL METHODS ###

    def __getattr__(self, attr):
        try:
            object.__getattr__(self, attr)
        except AttributeError:
            for i, input_name in enumerate(
                self._ordered_input_names):
                if input_name == attr:
                    return self.inputs[i]
        raise AttributeError

    def __getitem__(self, i):
        return self._output_proxies[i]

    def __len__(self):
        return 1

    def __repr__(self):
        from supriya.tools import synthdeftools
        if self.calculation_rate == synthdeftools.CalculationRate.DEMAND:
            return '{}()'.format(type(self).__name__)
        calculation_abbreviations = {
            synthdeftools.CalculationRate.AUDIO: 'ar',
            synthdeftools.CalculationRate.CONTROL: 'kr',
            synthdeftools.CalculationRate.SCALAR: 'ir',
            }
        string = '{}.{}()'.format(
            type(self).__name__,
            calculation_abbreviations[self.calculation_rate]
            )
        return string

    ### PRIVATE METHODS ###

    def _add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index=None):
        from supriya import synthdeftools
        if isinstance(ugen, synthdeftools.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = synthdeftools.OutputProxy(
                output_index=output_index,
                source=ugen,
                )
        source_ugen = output_proxy.source
        self._inputs.append(output_proxy)
        if self not in source_ugen.descendants:
            source_ugen.descendants.append(self)

    def _check_self_rate_as_first_input_rate(self):
        from supriya import synthdeftools
        first_input_rate = synthdeftools.CalculationRate.from_input(
            self.inputs[0],
            )
        return self.calculation_rate == first_input_rate

    def _check_range_of_inputs_at_audio_rate(self, start=None, stop=None):
        from supriya import synthdeftools
        if self.calculation_rate != synthdeftools.CalculationRate.AUDIO:
            return True
        for input_ in self.inputs[start:stop]:
            rate = synthdeftools.CalculationRate.from_input(input_)
            if rate != synthdeftools.CalculationRate.AUDIO:
                return False
        return True

    def _collect_constants(self):
        from supriya import synthdeftools
        for input_ in self._inputs:
            if not isinstance(input_, synthdeftools.OutputProxy):
                self.synthdef._add_constant(float(input_))

    def _configure_input(self, name, value):
        from supriya import synthdeftools
        if isinstance(value, (int, float)):
            self._add_constant_input(value)
        elif isinstance(value, (synthdeftools.OutputProxy, synthdeftools.UGen)):
            self._add_ugen_input(
                value._get_source(),
                value._get_output_number(),
                )
        elif isinstance(value, tuple) and \
            all(isinstance(_, (int, float)) for _ in value):
            assert self._unexpanded_input_names
            assert name in self._unexpanded_input_names
            for x in value:
                self._add_constant_input(x)
        else:
            raise Exception(value)

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate]

    def _get_source(self):
        return self

    def _initialize_topological_sort(self):
        from supriya import synthdeftools
        for input_ in self.inputs:
            if isinstance(input_, synthdeftools.OutputProxy):
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
    def _new_expanded(
        cls,
        calculation_rate=None,
        special_index=0,
        **kwargs
        ):
        import sys
        from supriya import synthdeftools
        if sys.version_info[0] == 2:
            import funcsigs
            get_signature = funcsigs.signature
        else:
            import inspect
            get_signature = inspect.signature
        #assert isinstance(calculation_rate, synthdeftools.CalculationRate)
        input_dicts = UGen.expand_dictionary(
            kwargs, unexpanded_input_names=cls._unexpanded_input_names)
        ugens = []
        signature = get_signature(cls.__init__)
        has_custom_special_index = 'special_index' in signature.parameters
        for input_dict in input_dicts:
            if has_custom_special_index:
                ugen = cls._new_single(
                    calculation_rate=calculation_rate,
                    special_index=special_index,
                    **input_dict
                    )
            else:
                ugen = cls._new_single(
                    calculation_rate=calculation_rate,
                    **input_dict
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdeftools.UGenArray(ugens)

    @classmethod
    def _new_single(
        cls,
        calculation_rate=None,
        **kwargs
        ):
        ugen = cls(
            calculation_rate=calculation_rate,
            **kwargs
            )
        return ugen

    def _optimize_graph(self):
        pass

    def _remove_antecedent(self, ugen):
        self.antecedents.remove(ugen)
        self._make_available()

    def _schedule(self, out_stack):
        for ugen in reversed(self.descendants):
            ugen._remove_antecedent(self)
        out_stack.append(self)

    def _validate_inputs(self):
        pass

    ### PUBLIC METHODS ###

    @staticmethod
    def as_audio_rate_input(expr):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        if isinstance(expr, (int, float)):
            if expr == 0:
                return ugentools.Silence.ar()
            return ugentools.DC.ar(expr)
        elif isinstance(expr, (synthdeftools.UGen, synthdeftools.OutputProxy)):
            if expr.calculation_rate == synthdeftools.CalculationRate.AUDIO:
                return expr
            return ugentools.K2A.ar(source=expr)
        elif isinstance(expr, collections.Iterable):
            return synthdeftools.UGenArray(
                UGen.as_audio_rate_input(x)
                for x in expr
                )
        raise ValueError(expr)

    def compile(self, synthdef):
        def compile_input_spec(i, synthdef):
            from supriya import synthdeftools
            result = []
            if isinstance(i, float):
                result.append(SynthDef._encode_unsigned_int_32bit(0xffffffff))
                constant_index = synthdef._get_constant_index(i)
                result.append(SynthDef._encode_unsigned_int_32bit(
                    constant_index))
            elif isinstance(i, synthdeftools.OutputProxy):
                ugen = i.source
                output_index = i.output_index
                ugen_index = synthdef._get_ugen_index(ugen)
                result.append(SynthDef._encode_unsigned_int_32bit(ugen_index))
                result.append(SynthDef._encode_unsigned_int_32bit(output_index))
            else:
                raise Exception('Unhandled input spec: {}'.format(i))
            return bytes().join(result)
        from supriya.tools.synthdeftools import SynthDef
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
        result = bytes().join(result)
        return result

    @staticmethod
    def expand_dictionary(dictionary, unexpanded_input_names=None):
        r'''Expands a dictionary into multichannel dictionaries.

        ::

            >>> import supriya
            >>> dictionary = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = supriya.synthdeftools.UGen.expand_dictionary(
            ...     dictionary)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> dictionary = {'bus': (8, 9), 'source': (1, 2, 3)}
            >>> result = supriya.synthdeftools.UGen.expand_dictionary(
            ...     dictionary,
            ...     unexpanded_input_names=('source',),
            ...     )
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bus', 8), ('source', (1, 2, 3))]
            [('bus', 9), ('source', (1, 2, 3))]

        '''
        dictionary = dictionary.copy()
        cached_unexpanded_inputs = {}
        if unexpanded_input_names is not None:
            for input_name in unexpanded_input_names:
                if input_name not in dictionary:
                    continue
                cached_unexpanded_inputs[input_name] = \
                    dictionary[input_name]
                del(dictionary[input_name])
        maximum_length = 1
        result = []
        for name, value in dictionary.items():
            if isinstance(value, collections.Sequence):
                maximum_length = max(maximum_length, len(value))
        for i in range(maximum_length):
            result.append({})
            for name, value in dictionary.items():
                if isinstance(value, collections.Sequence):
                    value = value[i % len(value)]
                    result[i][name] = value
                else:
                    result[i][name] = value
        for expanded_inputs in result:
            expanded_inputs.update(cached_unexpanded_inputs)
        return result

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
    def has_done_action(self):
        return 'done_action' in self._ordered_input_names

    @property
    def inputs(self):
        return tuple(self._inputs)

    @property
    def signal_range(self):
        from supriya.tools import synthdeftools
        return synthdeftools.SignalRange.BIPOLAR

    @property
    def special_index(self):
        return self._special_index

    @property
    def synthdef(self):
        return self._synthdef

    @synthdef.setter
    def synthdef(self, synthdef):
        from supriya.tools import synthdeftools
        assert isinstance(synthdef, synthdeftools.SynthDef)
        self._synthdef = synthdef

    @property
    def width_first_antecedents(self):
        return self._width_first_antecedents
