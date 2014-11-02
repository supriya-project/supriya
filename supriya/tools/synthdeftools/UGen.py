# -*- encoding: utf-8 -*-
from __future__ import print_function
import abc
import collections
from supriya.tools.synthdeftools.SignalRange import SignalRange
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class UGen(UGenMethodMixin):
    r'''A UGen.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    __slots__ = (
        '_calculation_rate',
        '_inputs',
        '_output_proxies',
        '_special_index',
        )

    _ordered_input_names = ()

    _signal_range = SignalRange.BIPOLAR

    _unexpanded_input_names = None

    _valid_rates = None

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        rate=None,
        special_index=0,
        **kwargs
        ):
        from supriya import servertools
        from supriya import synthdeftools
        assert isinstance(rate, synthdeftools.Rate), \
            rate
        if self._valid_rates is not None:
            assert rate in self._valid_rates
        self._calculation_rate = rate
        self._inputs = []
        self._special_index = special_index
        for i in range(len(self._ordered_input_names)):
            input_name = self._ordered_input_names[i]
            input_value = kwargs.get(input_name, None)
            if input_name in kwargs:
                input_value = kwargs[input_name]
                del(kwargs[input_name])
            prototype = (
                UGen,
                float,
                int,
                servertools.Buffer,
                servertools.BufferGroup,
                servertools.Bus,
                servertools.BusGroup,
                servertools.Node,
                synthdeftools.OutputProxy,
                synthdeftools.Parameter,
                )
            if self._unexpanded_input_names and \
                input_name in self._unexpanded_input_names:
                prototype += (tuple,)
            assert isinstance(input_value, prototype), \
                (input_name, input_value)
            self._configure_input(input_name, input_value)
        if kwargs:
            raise ValueError(kwargs)
        self._validate_inputs()
        self._output_proxies = tuple(
            synthdeftools.OutputProxy(self, i)
            for i in range(len(self))
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        r'''Gets output proxy at index `i`.

        ::

            >>> ugen = ugentools.SinOsc.ar()
            >>> ugen[0]
            OutputProxy(
                source=SinOsc(
                    rate=<Rate.AUDIO: 2>,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )
        
        Returns output proxy.
        '''
        return self._output_proxies[i]

    def __len__(self):
        r'''Gets number of ugen outputs.

        Returns integer.
        '''
        return 1

    def __repr__(self):
        r'''Gets interpreter representation of ugen.

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
        '''
        from supriya.tools import synthdeftools
        if self.rate == synthdeftools.Rate.DEMAND:
            return '{}()'.format(type(self).__name__)
        calculation_abbreviations = {
            synthdeftools.Rate.AUDIO: 'ar',
            synthdeftools.Rate.CONTROL: 'kr',
            synthdeftools.Rate.SCALAR: 'ir',
            }
        string = '{}.{}()'.format(
            type(self).__name__,
            calculation_abbreviations[self.rate]
            )
        return string

    def __str__(self):
        r'''Gets string format of ugen.

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
                2_BinaryOpUGen:MULTIPLICATION[0] -> 3_Out[1]
            }

        '''
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
        elif isinstance(expr, (synthdeftools.UGen, synthdeftools.OutputProxy)):
            if expr.rate == synthdeftools.Rate.AUDIO:
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
        if isinstance(ugen, synthdeftools.Parameter):
            output_proxy = ugen
        elif isinstance(ugen, synthdeftools.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = synthdeftools.OutputProxy(
                output_index=output_index,
                source=ugen,
                )
        self._inputs.append(output_proxy)

    def _check_rate_same_as_first_input_rate(self):
        from supriya import synthdeftools
        first_input_rate = synthdeftools.Rate.from_input(
            self.inputs[0],
            )
        return self.rate == first_input_rate

    def _check_range_of_inputs_at_audio_rate(self, start=None, stop=None):
        from supriya import synthdeftools
        if self.rate != synthdeftools.Rate.AUDIO:
            return True
        for input_ in self.inputs[start:stop]:
            rate = synthdeftools.Rate.from_input(input_)
            if rate != synthdeftools.Rate.AUDIO:
                return False
        return True

    def _configure_input(self, name, value):
        from supriya import servertools
        from supriya import synthdeftools
        if isinstance(value, (int, float)):
            self._add_constant_input(value)
        elif isinstance(value, (
            synthdeftools.OutputProxy,
            synthdeftools.Parameter,
            synthdeftools.UGen,
            )):
            self._add_ugen_input(
                value._get_source(),
                value._get_output_number(),
                )
        elif isinstance(value, (
            servertools.Bus,
            servertools.BusGroup,
            servertools.Buffer,
            servertools.BufferGroup,
            servertools.Node,
            )):
            self._add_constant_input(float(value))
        elif isinstance(value, tuple) and \
            all(isinstance(_, (int, float)) for _ in value):
            assert self._unexpanded_input_names
            assert name in self._unexpanded_input_names
            for x in value:
                self._add_constant_input(x)
        else:
            raise Exception(value)

    @staticmethod
    def _expand_dictionary(dictionary, unexpanded_input_names=None):
        r'''Expands a dictionary into multichannel dictionaries.

        ::

            >>> dictionary = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = synthdeftools.UGen._expand_dictionary(
            ...     dictionary)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> dictionary = {'bus': (8, 9), 'source': (1, 2, 3)}
            >>> result = synthdeftools.UGen._expand_dictionary(
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

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.rate] * len(self)

    def _get_source(self):
        return self

    @classmethod
    def _new_expanded(
        cls,
        rate=None,
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
        input_dicts = UGen._expand_dictionary(
            kwargs, unexpanded_input_names=cls._unexpanded_input_names)
        ugens = []
        signature = get_signature(cls.__init__)
        has_custom_special_index = 'special_index' in signature.parameters
        for input_dict in input_dicts:
            if has_custom_special_index:
                ugen = cls._new_single(
                    rate=rate,
                    special_index=special_index,
                    **input_dict
                    )
            else:
                ugen = cls._new_single(
                    rate=rate,
                    **input_dict
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdeftools.UGenArray(ugens)

    @classmethod
    def _new_single(
        cls,
        rate=None,
        **kwargs
        ):
        ugen = cls(
            rate=rate,
            **kwargs
            )
        return ugen

    def _optimize_graph(self):
        pass

    def _validate_inputs(self):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _has_done_action(self):
        return 'done_action' in self._ordered_input_names

    ### PUBLIC PROPERTIES ###

    @property
    def inputs(self):
        r'''Gets inputs of ugen.

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
                    rate=<Rate.CONTROL: 1>
                    ),
                output_index=0
                )
            0.5

        Returns tuple.
        '''
        return tuple(self._inputs)

    @property
    def outputs(self):
        r'''Gets outputs of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar(
            ...     frequency=ugentools.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> ugen.outputs
            (<Rate.AUDIO: 2>,)

        Returns tuple.
        '''
        return tuple(self._get_outputs())

    @property
    def rate(self):
        r'''Gets calculation rate of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar(
            ...     frequency=ugentools.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> ugen.rate
            <Rate.AUDIO: 2>

        Returns calculation rate.
        '''
        return self._calculation_rate

    @property
    def signal_range(self):
        r'''Gets signal range of ugen.

        ::

            >>> ugen = ugentools.SinOsc.ar()
            >>> ugen.signal_range
            <SignalRange.BIPOLAR: 1>

        A bipolar signal range indicates that the ugen generates signals above
        and below zero.
        
        A unipolar signal range indicates that the ugen only generates signals
        of 0 or greater.

        Returns signal range.
        '''
        return self._signal_range

    @property
    def special_index(self):
        r'''Gets special index of ugen.

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
        '''
        return self._special_index