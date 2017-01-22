# -*- encoding: utf-8 -*-
from __future__ import print_function
import abc
import collections
import six
from supriya.tools.synthdeftools.SignalRange import SignalRange
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class UGen(UGenMethodMixin):
    """
    A UGen.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = (
        '_calculation_rate',
        '_inputs',
        '_special_index',
        '_uuid',
        )

    _ordered_input_names = ()

    _signal_range = SignalRange.BIPOLAR

    _unexpanded_input_names = None

    _valid_rates = None

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
        if self._valid_rates is not None:
            assert calculation_rate in self._valid_rates
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._special_index = special_index
        ugenlike_prototype = (
            UGen,
            synthdeftools.Parameter,
            )
        for i in range(len(self._ordered_input_names)):
            input_name = self._ordered_input_names[i]
            input_value = kwargs.get(input_name, None)
            if input_name in kwargs:
                input_value = kwargs[input_name]
                del(kwargs[input_name])
            if isinstance(input_value, ugenlike_prototype):
                assert len(input_value) == 1
                input_value = input_value[0]
            if self._is_unexpanded_input_name(input_name):
                if isinstance(input_value, collections.Sequence):
                    input_value = tuple(input_value)
                elif not self._is_valid_input(input_value):
                    raise ValueError(input_name, input_value)
            elif not self._is_valid_input(input_value):
                raise ValueError(input_name, input_value)
            self._configure_input(input_name, input_value)
        if kwargs:
            raise ValueError(kwargs)
        assert all(isinstance(_, (synthdeftools.OutputProxy, float))
            for _ in self.inputs)
        self._validate_inputs()
        self._uuid = None
        if synthdeftools.SynthDefBuilder._active_builders:
            builder = synthdeftools.SynthDefBuilder._active_builders[-1]
            self._uuid = builder._uuid
        self._check_inputs_share_same_uuid()
        if self._uuid is not None:
            builder._add_ugens(self)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        """
        Gets output proxy at index `i`.

        ::

            >>> ugen = ugentools.SinOsc.ar()
            >>> ugen[0]
            OutputProxy(
                source=SinOsc(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns output proxy.
        """
        return self._get_output_proxy(i)

    def __len__(self):
        """
        Gets number of ugen outputs.

        Returns integer.
        """
        return 1

    def __repr__(self):
        """
        Gets interpreter representation of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar()
            >>> repr(ugen)
            'SinOsc.ar()'

        ::

            >>> ugen = ugentools.WhiteNoise.kr()
            >>> repr(ugen)
            'WhiteNoise.kr()'

        ::

            >>> ugen = ugentools.Rand.ir()
            >>> repr(ugen)
            'Rand.ir()'

        Returns string.
        """
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

    def __str__(self):
        """
        Gets string format of ugen.

        ::

            >>> sin_osc_a = ugentools.SinOsc.ar()
            >>> sin_osc_b = ugentools.SinOsc.ar(frequency=443)
            >>> multiplied = sin_osc_a * sin_osc_b
            >>> output = ugentools.Out.ar(source=multiplied)

        ::

            >>> print(str(output))
            SynthDef 221d0a5d0c162c5b9d3d1fd74ffb83ff {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                const_2:443.0 -> 1_SinOsc[0:frequency]
                const_1:0.0 -> 1_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:MULTIPLICATION[0:left]
                1_SinOsc[0] -> 2_BinaryOpUGen:MULTIPLICATION[1:right]
                const_1:0.0 -> 3_Out[0:bus]
                2_BinaryOpUGen:MULTIPLICATION[0] -> 3_Out[1:source]
            }

        """
        return UGenMethodMixin.__str__(self)

    ### PRIVATE METHODS ###

    @staticmethod
    def _as_audio_rate_input(expr):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        if isinstance(expr, (int, float)):
            if expr == 0:
                return ugentools.Silence.ar()
            return ugentools.DC.ar(expr)
        elif isinstance(expr, (UGen, synthdeftools.OutputProxy)):
            if expr.calculation_rate == synthdeftools.CalculationRate.AUDIO:
                return expr
            return ugentools.K2A.ar(source=expr)
        elif isinstance(expr, collections.Iterable):
            return synthdeftools.UGenArray(
                UGen._as_audio_rate_input(x)
                for x in expr
                )
        raise ValueError(expr)

    def _add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index=None):
        from supriya import synthdeftools
        #if isinstance(ugen, synthdeftools.Parameter):
        #    output_proxy = ugen
        if isinstance(ugen, synthdeftools.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = synthdeftools.OutputProxy(
                output_index=output_index,
                source=ugen,
                )
        self._inputs.append(output_proxy)

    def _check_inputs_share_same_uuid(self):
        from supriya.tools import synthdeftools
        for input_ in self.inputs:
            if not isinstance(input_, synthdeftools.OutputProxy):
                continue
            if input_.source._uuid != self._uuid:
                message = 'UGen input in different scope: {!r}'
                message = message.format(input_.source)
                raise ValueError(message)

    def _check_rate_same_as_first_input_rate(self):
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
            calculation_rate = synthdeftools.CalculationRate.from_input(input_)
            if calculation_rate != synthdeftools.CalculationRate.AUDIO:
                return False
        return True

    def _configure_input(self, name, value):
        from supriya import synthdeftools
        ugen_prototype = (
            synthdeftools.OutputProxy,
            synthdeftools.Parameter,
            UGen,
            )
        if hasattr(value, '__float__'):
            self._add_constant_input(float(value))
        elif isinstance(value, ugen_prototype):
            self._add_ugen_input(
                value._get_source(),
                value._get_output_number(),
                )
        elif isinstance(value, tuple):
            assert self._unexpanded_input_names
            assert name in self._unexpanded_input_names
            for x in value:
                if hasattr(x, '__float__'):
                    self._add_constant_input(float(x))
                elif isinstance(x, ugen_prototype):
                    self._add_ugen_input(
                        x._get_source(),
                        x._get_output_number(),
                        )
                else:
                    raise Exception(repr(value, x))
        else:
            raise Exception(repr(value))

    @staticmethod
    def _expand_dictionary(dictionary, unexpanded_input_names=None):
        """
        Expands a dictionary into multichannel dictionaries.

        ::

            >>> dictionary = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = ugentools.UGen._expand_dictionary(
            ...     dictionary)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> dictionary = {'bus': (8, 9), 'source': (1, 2, 3)}
            >>> result = ugentools.UGen._expand_dictionary(
            ...     dictionary,
            ...     unexpanded_input_names=('source',),
            ...     )
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bus', 8), ('source', (1, 2, 3))]
            [('bus', 9), ('source', (1, 2, 3))]

        """
        from supriya.tools import synthdeftools
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
        prototype = (
            collections.Sequence,
            UGen,
            synthdeftools.Parameter,
            )
        for name, value in dictionary.items():
            if isinstance(value, prototype) and \
                not isinstance(value, six.string_types):
                maximum_length = max(maximum_length, len(value))
        for i in range(maximum_length):
            result.append({})
            for name, value in dictionary.items():
                if isinstance(value, prototype) and \
                    not isinstance(value, six.string_types):
                    value = value[i % len(value)]
                    result[i][name] = value
                else:
                    result[i][name] = value
        for expanded_inputs in result:
            expanded_inputs.update(cached_unexpanded_inputs)
        return result

    def _get_done_action(self):
        from supriya.tools import synthdeftools
        if 'done_action' not in self._ordered_input_names:
            return None
        return synthdeftools.DoneAction.from_expr(int(self.done_action))

    @staticmethod
    def _get_method_for_rate(cls, calculation_rate):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.from_input(
            calculation_rate)
        if calculation_rate == synthdeftools.CalculationRate.AUDIO:
            return cls.ar
        elif calculation_rate == synthdeftools.CalculationRate.CONTROL:
            return cls.kr
        elif calculation_rate == synthdeftools.CalculationRate.SCALAR:
            if hasattr(cls, 'ir'):
                return cls.ir
            return cls.kr
        return cls.new

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    def _get_source(self):
        return self

    def _is_unexpanded_input_name(self, input_name):
        if self._unexpanded_input_names:
            if input_name in self._unexpanded_input_names:
                return True
        return False

    def _is_valid_input(self, input_value):
        from supriya import synthdeftools
        if isinstance(input_value, synthdeftools.OutputProxy):
            return True
        elif hasattr(input_value, '__float__'):
            return True
        return False

    @classmethod
    def _new_expanded(
        cls,
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
        signature = get_signature(cls.__init__)
        input_dicts = UGen._expand_dictionary(
            kwargs, unexpanded_input_names=cls._unexpanded_input_names)
        ugens = []
        has_custom_special_index = 'special_index' in signature.parameters
        for input_dict in input_dicts:
            if has_custom_special_index:
                ugen = cls._new_single(
                    special_index=special_index,
                    **input_dict
                    )
            else:
                ugen = cls._new_single(
                    **input_dict
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdeftools.UGenArray(ugens)

    @classmethod
    def _new_single(
        cls,
        **kwargs
        ):
        ugen = cls(
            **kwargs
            )
        return ugen

    def _optimize_graph(self, sort_bundles):
        pass

    def _perform_dead_code_elimination(self, sort_bundles):
        sort_bundle = sort_bundles.get(self, None)
        if not sort_bundle or sort_bundle.descendants:
            return
        del(sort_bundles[self])
        for antecedent in tuple(sort_bundle.antecedents):
            antecedent_bundle = sort_bundles.get(antecedent, None)
            if not antecedent_bundle:
                continue
            antecedent_bundle.descendants.remove(self)
            antecedent._optimize_graph(sort_bundles)

    def _validate_inputs(self):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _has_done_action(self):
        return 'done_action' in self._ordered_input_names

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        """
        Gets calculation-rate of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar(
            ...     frequency=ugentools.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> ugen.calculation_rate
            CalculationRate.AUDIO

        Returns calculation-rate.
        """
        return self._calculation_rate

    @property
    def has_done_flag(self):
        return False

    @property
    def inputs(self):
        """
        Gets inputs of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar(
            ...     frequency=ugentools.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> for input_ in ugen.inputs:
            ...     input_
            ...
            OutputProxy(
                source=WhiteNoise(
                    calculation_rate=CalculationRate.CONTROL
                    ),
                output_index=0
                )
            0.5

        Returns tuple.
        """
        return tuple(self._inputs)

    @property
    def is_input_ugen(self):
        return False

    @property
    def is_output_ugen(self):
        return False

    @property
    def outputs(self):
        """
        Gets outputs of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar(
            ...     frequency=ugentools.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> ugen.outputs
            (CalculationRate.AUDIO,)

        Returns tuple.
        """
        return tuple(self._get_outputs())

    @property
    def signal_range(self):
        """
        Gets signal range of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar()
            >>> ugen.signal_range
            SignalRange.BIPOLAR

        A bipolar signal range indicates that the ugen generates signals above
        and below zero.

        A unipolar signal range indicates that the ugen only generates signals
        of 0 or greater.

        Returns signal range.
        """
        return self._signal_range

    @property
    def special_index(self):
        """
        Gets special index of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar(
            ...     frequency=ugentools.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> ugen.special_index
            0

        The `special index` of most ugens will be 0. SuperColliders's synth
        definition file format uses the special index to store the operator id
        for binary and unary operator ugens, and the parameter index of
        controls.

        Returns integer.
        """
        return self._special_index
