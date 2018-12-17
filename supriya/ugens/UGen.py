import abc
import collections
import inspect
from typing import Optional, Tuple

from supriya.synthdefs.SignalRange import SignalRange
from supriya.synthdefs.UGenMethodMixin import UGenMethodMixin
from supriya.typing import UGenInputMap
from supriya.ugens.UGenMeta import UGenMeta


class UGen(UGenMethodMixin, metaclass=UGenMeta):
    """
    A UGen.
    """

    ### CLASS VARIABLES ###

    __documentation_section__: Optional[str] = "SynthDef Internals"

    __slots__ = ("_inputs", "_special_index", "_uuid")

    _default_channel_count = 1

    _has_settable_channel_count = False

    _has_done_flag = False

    _is_input = False

    _is_output = False

    _is_pure = False

    _is_width_first = False

    _ordered_input_names: UGenInputMap = None

    _signal_range: int = SignalRange.BIPOLAR

    _unexpanded_input_names: Tuple[str, ...] = ()

    _valid_calculation_rates: Tuple[int, ...] = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, calculation_rate=None, special_index=0, **kwargs):
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        if self._valid_calculation_rates:
            assert calculation_rate in self._valid_calculation_rates
        self._calculation_rate = calculation_rate
        self._inputs = []
        self._special_index = special_index
        ugenlike_prototype = (UGen, supriya.synthdefs.Parameter)
        server_id_prototype = (
            supriya.realtime.ServerObjectProxy,
            supriya.realtime.BusProxy,
            supriya.realtime.BufferProxy,
        )
        for input_name in self._ordered_input_names:
            input_value = None
            if input_name in kwargs:
                input_value = kwargs.pop(input_name)
            if isinstance(input_value, ugenlike_prototype):
                assert len(input_value) == 1
                input_value = input_value[0]
            elif isinstance(input_value, server_id_prototype):
                input_value = int(input_value)
            if self._is_unexpanded_input_name(input_name):
                if not isinstance(input_value, collections.Sequence):
                    input_value = (input_value,)
                if isinstance(input_value, collections.Sequence):
                    input_value = tuple(input_value)
                elif not self._is_valid_input(input_value):
                    raise ValueError(input_name, input_value)
            elif not self._is_valid_input(input_value):
                raise ValueError(input_name, input_value)
            self._configure_input(input_name, input_value)
        if kwargs:
            raise ValueError(kwargs)
        assert all(
            isinstance(_, (supriya.synthdefs.OutputProxy, float)) for _ in self.inputs
        )
        self._validate_inputs()
        self._uuid = None
        if supriya.synthdefs.SynthDefBuilder._active_builders:
            builder = supriya.synthdefs.SynthDefBuilder._active_builders[-1]
            self._uuid = builder._uuid
        self._check_inputs_share_same_uuid()
        if self._uuid is not None:
            builder._add_ugens(self)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        """
        Gets output proxy at index `i`.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar()
            >>> ugen[0]
            SinOsc.ar()[0]

        Returns output proxy.
        """
        return self._get_output_proxy(i)

    def __len__(self):
        """
        Gets number of ugen outputs.

        Returns integer.
        """
        return getattr(self, "_channel_count", self._default_channel_count)

    def __repr__(self):
        """
        Gets interpreter representation of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar()
            >>> repr(ugen)
            'SinOsc.ar()'

        ::

            >>> ugen = supriya.ugens.WhiteNoise.kr()
            >>> repr(ugen)
            'WhiteNoise.kr()'

        ::

            >>> ugen = supriya.ugens.Rand.ir()
            >>> repr(ugen)
            'Rand.ir()'

        Returns string.
        """
        import supriya.synthdefs

        if self.calculation_rate == supriya.CalculationRate.DEMAND:
            return "{}()".format(type(self).__name__)
        calculation_abbreviations = {
            supriya.CalculationRate.AUDIO: "ar",
            supriya.CalculationRate.CONTROL: "kr",
            supriya.CalculationRate.SCALAR: "ir",
        }
        string = "{}.{}()".format(
            type(self).__name__, calculation_abbreviations[self.calculation_rate]
        )
        return string

    ### PRIVATE METHODS ###

    @staticmethod
    def _as_audio_rate_input(expr):
        import supriya.synthdefs
        import supriya.ugens

        if isinstance(expr, (int, float)):
            if expr == 0:
                return supriya.ugens.Silence.ar()
            return supriya.ugens.DC.ar(expr)
        elif isinstance(expr, (UGen, supriya.synthdefs.OutputProxy)):
            if expr.calculation_rate == supriya.CalculationRate.AUDIO:
                return expr
            return supriya.ugens.K2A.ar(source=expr)
        elif isinstance(expr, collections.Iterable):
            return supriya.synthdefs.UGenArray(
                UGen._as_audio_rate_input(x) for x in expr
            )
        raise ValueError(expr)

    def _add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index=None):
        import supriya.synthdefs

        # if isinstance(ugen, supriya.synthdefs.Parameter):
        #    output_proxy = ugen
        if isinstance(ugen, supriya.synthdefs.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = supriya.synthdefs.OutputProxy(
                output_index=output_index, source=ugen
            )
        self._inputs.append(output_proxy)

    def _check_inputs_share_same_uuid(self):
        import supriya.synthdefs

        for input_ in self.inputs:
            if not isinstance(input_, supriya.synthdefs.OutputProxy):
                continue
            if input_.source._uuid != self._uuid:
                message = "UGen input in different scope: {!r}"
                message = message.format(input_.source)
                raise ValueError(message)

    def _check_rate_same_as_first_input_rate(self):
        import supriya.synthdefs

        first_input_rate = supriya.CalculationRate.from_expr(self.inputs[0])
        return self.calculation_rate == first_input_rate

    def _check_range_of_inputs_at_audio_rate(self, start=None, stop=None):
        import supriya.synthdefs

        if self.calculation_rate != supriya.CalculationRate.AUDIO:
            return True
        for input_ in self.inputs[start:stop]:
            calculation_rate = supriya.CalculationRate.from_expr(input_)
            if calculation_rate != supriya.CalculationRate.AUDIO:
                return False
        return True

    def _configure_input(self, name, value):
        import supriya.synthdefs

        ugen_prototype = (
            supriya.synthdefs.OutputProxy,
            supriya.synthdefs.Parameter,
            UGen,
        )
        if hasattr(value, "__float__"):
            self._add_constant_input(float(value))
        elif isinstance(value, ugen_prototype):
            self._add_ugen_input(value._get_source(), value._get_output_number())
        elif isinstance(value, tuple):
            assert self._unexpanded_input_names
            assert name in self._unexpanded_input_names
            for x in value:
                if hasattr(x, "__float__"):
                    self._add_constant_input(float(x))
                elif isinstance(x, ugen_prototype):
                    self._add_ugen_input(x._get_source(), x._get_output_number())
                else:
                    raise Exception("{!r} {!r}".format(value, x))
        else:
            raise Exception(repr(value))

    @staticmethod
    def _expand_dictionary(dictionary, unexpanded_input_names=None):
        """
        Expands a dictionary into multichannel dictionaries.

        ::

            >>> dictionary = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = supriya.ugens.UGen._expand_dictionary(
            ...     dictionary)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> dictionary = {'bus': (8, 9), 'source': (1, 2, 3)}
            >>> result = supriya.ugens.UGen._expand_dictionary(
            ...     dictionary,
            ...     unexpanded_input_names=('source',),
            ...     )
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bus', 8), ('source', (1, 2, 3))]
            [('bus', 9), ('source', (1, 2, 3))]

        """
        import supriya.synthdefs

        dictionary = dictionary.copy()
        cached_unexpanded_inputs = {}
        if unexpanded_input_names is not None:
            for input_name in unexpanded_input_names:
                if input_name not in dictionary:
                    continue
                cached_unexpanded_inputs[input_name] = dictionary[input_name]
                del (dictionary[input_name])
        maximum_length = 1
        result = []
        prototype = (collections.Sequence, UGen, supriya.synthdefs.Parameter)
        for name, value in dictionary.items():
            if isinstance(value, prototype) and not isinstance(value, str):
                maximum_length = max(maximum_length, len(value))
        for i in range(maximum_length):
            result.append({})
            for name, value in dictionary.items():
                if isinstance(value, prototype) and not isinstance(value, str):
                    value = value[i % len(value)]
                    result[i][name] = value
                else:
                    result[i][name] = value
        for expanded_inputs in result:
            expanded_inputs.update(cached_unexpanded_inputs)
        return result

    def _get_done_action(self):
        import supriya.synthdefs

        if "done_action" not in self._ordered_input_names:
            return None
        return supriya.synthdefs.DoneAction.from_expr(int(self.done_action))

    @staticmethod
    def _get_method_for_rate(cls, calculation_rate):
        import supriya.synthdefs

        calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        if calculation_rate == supriya.CalculationRate.AUDIO:
            return cls.ar
        elif calculation_rate == supriya.CalculationRate.CONTROL:
            return cls.kr
        elif calculation_rate == supriya.CalculationRate.SCALAR:
            if hasattr(cls, "ir"):
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
        import supriya.synthdefs

        if isinstance(input_value, supriya.synthdefs.OutputProxy):
            return True
        elif hasattr(input_value, "__float__"):
            return True
        return False

    @classmethod
    def _new_expanded(cls, special_index=0, **kwargs):
        import supriya.synthdefs

        get_signature = inspect.signature
        signature = get_signature(cls.__init__)
        input_dicts = UGen._expand_dictionary(
            kwargs, unexpanded_input_names=cls._unexpanded_input_names
        )
        ugens = []
        has_custom_special_index = "special_index" in signature.parameters
        for input_dict in input_dicts:
            if has_custom_special_index:
                ugen = cls._new_single(special_index=special_index, **input_dict)
            else:
                ugen = cls._new_single(**input_dict)
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return supriya.synthdefs.UGenArray(ugens)

    @classmethod
    def _new_single(cls, **kwargs):
        ugen = cls(**kwargs)
        return ugen

    def _optimize_graph(self, sort_bundles):
        pass

    def _perform_dead_code_elimination(self, sort_bundles):
        sort_bundle = sort_bundles.get(self, None)
        if not sort_bundle or sort_bundle.descendants:
            return
        del (sort_bundles[self])
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
        return "done_action" in self._ordered_input_names

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        """
        Gets calculation-rate of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> ugen.calculation_rate
            CalculationRate.AUDIO

        Returns calculation-rate.
        """
        return self._calculation_rate

    @property
    def has_done_flag(self):
        return self._has_done_flag

    @property
    def inputs(self):
        """
        Gets inputs of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
            ...     phase=0.5,
            ...     )
            >>> for input_ in ugen.inputs:
            ...     input_
            ...
            WhiteNoise.kr()[0]
            0.5

        Returns tuple.
        """
        return tuple(self._inputs)

    @property
    def is_input_ugen(self):
        return self._is_input

    @property
    def is_output_ugen(self):
        return self._is_output

    @property
    def outputs(self):
        """
        Gets outputs of ugen.

        ::

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
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

            >>> ugen = supriya.ugens.SinOsc.ar()
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

            >>> ugen = supriya.ugens.SinOsc.ar(
            ...     frequency=supriya.ugens.WhiteNoise.kr(),
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
