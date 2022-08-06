import collections
import struct
from collections.abc import Sequence

from supriya import CalculationRate, ParameterRate, utils
from supriya.system import SupriyaObject

from .bases import MultiOutUGen, UGen


class SynthDefCompiler(SupriyaObject):

    ### PUBLIC METHODS ###

    @staticmethod
    def compile_synthdef(synthdef, name):
        result = SynthDefCompiler.encode_string(name)
        result += synthdef._compiled_ugen_graph
        return result

    @staticmethod
    def compile_parameters(synthdef):
        result = []
        result.append(
            SynthDefCompiler.encode_unsigned_int_32bit(
                sum(len(_[1]) for _ in synthdef.indexed_parameters)
            )
        )
        for control_ugen in synthdef.control_ugens:
            for parameter in control_ugen.parameters:
                value = parameter.value
                if not isinstance(value, tuple):
                    value = (value,)
                for x in value:
                    result.append(SynthDefCompiler.encode_float(x))
        result.append(
            SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.indexed_parameters))
        )
        for index, parameter in synthdef.indexed_parameters:
            name = parameter.name
            result.append(SynthDefCompiler.encode_string(name))
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(index))
        return bytes().join(result)

    @staticmethod
    def compile_synthdefs(synthdefs, use_anonymous_names=False):
        def flatten(value):
            if isinstance(value, Sequence) and not isinstance(
                value, (bytes, bytearray)
            ):
                return bytes().join(flatten(x) for x in value)
            return value

        result = []
        encoded_file_type_id = b"SCgf"
        result.append(encoded_file_type_id)
        encoded_file_version = SynthDefCompiler.encode_unsigned_int_32bit(2)
        result.append(encoded_file_version)
        encoded_synthdef_count = SynthDefCompiler.encode_unsigned_int_16bit(
            len(synthdefs)
        )
        result.append(encoded_synthdef_count)
        for synthdef in synthdefs:
            name = synthdef.name
            if not name or use_anonymous_names:
                name = synthdef.anonymous_name
            result.append(SynthDefCompiler.compile_synthdef(synthdef, name))
        result = flatten(result)
        result = bytes(result)
        return result

    @staticmethod
    def compile_ugen(ugen, synthdef):
        outputs = ugen._get_outputs()
        result = []
        result.append(SynthDefCompiler.encode_string(type(ugen).__name__))
        result.append(SynthDefCompiler.encode_unsigned_int_8bit(ugen.calculation_rate))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(ugen.inputs)))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(outputs)))
        result.append(
            SynthDefCompiler.encode_unsigned_int_16bit(int(ugen.special_index))
        )
        for input_ in ugen.inputs:
            result.append(SynthDefCompiler.compile_ugen_input_spec(input_, synthdef))
        for output in outputs:
            result.append(SynthDefCompiler.encode_unsigned_int_8bit(output))
        result = bytes().join(result)
        return result

    @staticmethod
    def compile_ugen_graph(synthdef):
        result = []
        result.append(
            SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.constants))
        )
        for constant in synthdef.constants:
            result.append(SynthDefCompiler.encode_float(constant))
        result.append(SynthDefCompiler.compile_parameters(synthdef))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.ugens)))
        for ugen_index, ugen in enumerate(synthdef.ugens):
            result.append(SynthDefCompiler.compile_ugen(ugen, synthdef))
        result.append(SynthDefCompiler.encode_unsigned_int_16bit(0))
        result = bytes().join(result)
        return result

    @staticmethod
    def compile_ugen_input_spec(input_, synthdef):
        import supriya.synthdefs

        result = []
        if isinstance(input_, float):
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(0xFFFFFFFF))
            constant_index = synthdef._constants.index(input_)
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(constant_index))
        elif isinstance(input_, supriya.synthdefs.OutputProxy):
            ugen = input_.source
            output_index = input_.output_index
            ugen_index = synthdef._ugens.index(ugen)
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(ugen_index))
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(output_index))
        else:
            raise Exception("Unhandled input spec: {}".format(input_))
        return bytes().join(result)

    @staticmethod
    def encode_string(value):
        result = bytes(struct.pack(">B", len(value)))
        result += bytes(bytearray(value, encoding="ascii"))
        return result

    @staticmethod
    def encode_float(value):
        return bytes(struct.pack(">f", float(value)))

    @staticmethod
    def encode_unsigned_int_8bit(value):
        return bytes(struct.pack(">B", int(value)))

    @staticmethod
    def encode_unsigned_int_16bit(value):
        return bytes(struct.pack(">H", int(value)))

    @staticmethod
    def encode_unsigned_int_32bit(value):
        return bytes(struct.pack(">I", int(value)))


class SynthDefDecompiler(SupriyaObject):
    """
    SynthDef decompiler.

    ::

        >>> import supriya.synthdefs
        >>> import supriya.ugens
        >>> with supriya.synthdefs.SynthDefBuilder(
        ...     frequency=440,
        ...     trigger=supriya.synthdefs.Parameter(
        ...         value=0.0,
        ...         parameter_rate=supriya.ParameterRate.TRIGGER,
        ...     ),
        ... ) as builder:
        ...     sin_osc = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        ...     decay = supriya.ugens.Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder["trigger"],
        ...     )
        ...     enveloped_sin = sin_osc * decay
        ...     out = supriya.ugens.Out.ar(bus=0, source=enveloped_sin)
        ...
        >>> synthdef = builder.build()
        >>> supriya.graph(synthdef)  # doctest: +SKIP

    ::

        >>> print(synthdef)
        synthdef:
            name: 001520731aee5371fefab6b505cf64dd
            ugens:
            -   TrigControl.kr: null
            -   Decay.kr:
                    source: TrigControl.kr[0:trigger]
                    decay_time: 0.5
            -   Control.kr: null
            -   SinOsc.ar:
                    frequency: Control.kr[0:frequency]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: SinOsc.ar[0]
                    right: Decay.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]

    ::

        >>> compiled_synthdef = synthdef.compile()
        >>> sdd = supriya.synthdefs.SynthDefDecompiler
        >>> decompiled_synthdef = sdd.decompile_synthdefs(compiled_synthdef)[0]
        >>> supriya.graph(decompiled_synthdef)  # doctest: +SKIP

    ::

        >>> print(decompiled_synthdef)
        synthdef:
            name: 001520731aee5371fefab6b505cf64dd
            ugens:
            -   TrigControl.kr: null
            -   Decay.kr:
                    source: TrigControl.kr[0:trigger]
                    decay_time: 0.5
            -   Control.kr: null
            -   SinOsc.ar:
                    frequency: Control.kr[0:frequency]
                    phase: 0.0
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: SinOsc.ar[0]
                    right: Decay.kr[0]
            -   Out.ar:
                    bus: 0.0
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]

    ::

        >>> str(synthdef) == str(decompiled_synthdef)
        True

    """

    ### PRIVATE METHODS ###

    @staticmethod
    def _decode_constants(value, index):
        sdd = SynthDefDecompiler
        constants = []
        constants_count, index = sdd._decode_int_32bit(value, index)
        for _ in range(constants_count):
            constant, index = sdd._decode_float(value, index)
            constants.append(constant)
        return constants, index

    @staticmethod
    def _decode_parameters(value, index):
        import supriya.synthdefs

        sdd = SynthDefDecompiler
        parameter_values = []
        parameter_count, index = sdd._decode_int_32bit(value, index)
        for _ in range(parameter_count):
            parameter_value, index = sdd._decode_float(value, index)
            parameter_values.append(parameter_value)
        parameter_count, index = sdd._decode_int_32bit(value, index)
        parameter_names = []
        parameter_indices = []
        for _ in range(parameter_count):
            parameter_name, index = sdd._decode_string(value, index)
            parameter_index, index = sdd._decode_int_32bit(value, index)
            parameter_names.append(parameter_name)
            parameter_indices.append(parameter_index)
        indexed_parameters = []
        if parameter_count:
            pairs = tuple(zip(parameter_indices, parameter_names))
            pairs = sorted(pairs, key=lambda x: x[0])
            iterator = utils.iterate_nwise(pairs)
            for (index_one, name_one), (index_two, name_two) in iterator:
                value = parameter_values[index_one:index_two]
                if len(value) == 1:
                    value = value[0]
                parameter = supriya.synthdefs.Parameter(name=name_one, value=value)
                indexed_parameters.append((index_one, parameter))
            index_one, name_one = pairs[-1]
            value = parameter_values[index_one:]
            if len(value) == 1:
                value = value[0]
            parameter = supriya.synthdefs.Parameter(name=name_one, value=value)
            indexed_parameters.append((index_one, parameter))
            indexed_parameters.sort(key=lambda x: parameter_names.index(x[1].name))
        indexed_parameters = collections.OrderedDict(indexed_parameters)
        return indexed_parameters, index

    @staticmethod
    def _decompile_synthdef(value, index):
        import supriya.synthdefs
        import supriya.ugens

        sdd = SynthDefDecompiler
        synthdef = None
        name, index = sdd._decode_string(value, index)
        constants, index = sdd._decode_constants(value, index)
        indexed_parameters, index = sdd._decode_parameters(value, index)
        ugens = []
        ugen_count, index = sdd._decode_int_32bit(value, index)
        for i in range(ugen_count):
            ugen_name, index = sdd._decode_string(value, index)
            calculation_rate, index = sdd._decode_int_8bit(value, index)
            calculation_rate = supriya.CalculationRate(calculation_rate)
            input_count, index = sdd._decode_int_32bit(value, index)
            output_count, index = sdd._decode_int_32bit(value, index)
            special_index, index = sdd._decode_int_16bit(value, index)
            inputs = []
            for _ in range(input_count):
                ugen_index, index = sdd._decode_int_32bit(value, index)
                if ugen_index == 0xFFFFFFFF:
                    constant_index, index = sdd._decode_int_32bit(value, index)
                    constant_index = int(constant_index)
                    inputs.append(constants[constant_index])
                else:
                    ugen = ugens[ugen_index]
                    ugen_output_index, index = sdd._decode_int_32bit(value, index)
                    output_proxy = ugen[ugen_output_index]
                    inputs.append(output_proxy)
            for _ in range(output_count):
                output_rate, index = sdd._decode_int_8bit(value, index)
            ugen_class = getattr(supriya.ugens, ugen_name, None)
            if ugen_class is None:
                ugen_class = getattr(supriya.synthdefs, ugen_name)
            ugen = supriya.synthdefs.UGen.__new__(ugen_class)
            if issubclass(ugen_class, supriya.synthdefs.Control):
                starting_control_index = special_index
                parameters = sdd._collect_parameters_for_control(
                    calculation_rate,
                    indexed_parameters,
                    inputs,
                    output_count,
                    starting_control_index,
                    ugen_class,
                )
                ugen_class.__init__(
                    ugen,
                    parameters=parameters,
                    starting_control_index=starting_control_index,
                    calculation_rate=calculation_rate,
                )
            else:
                kwargs = {}
                if not ugen._unexpanded_input_names:
                    for i, input_name in enumerate(ugen._ordered_input_names):
                        kwargs[input_name] = inputs[i]
                else:
                    for i, input_name in enumerate(ugen._ordered_input_names):
                        if input_name not in ugen._unexpanded_input_names:
                            kwargs[input_name] = inputs[i]
                        else:
                            kwargs[input_name] = tuple(inputs[i:])
                if issubclass(ugen_class, MultiOutUGen):
                    MultiOutUGen.__init__(
                        ugen,
                        calculation_rate=calculation_rate,
                        channel_count=output_count,
                        special_index=special_index,
                        **kwargs,
                    )
                else:
                    UGen.__init__(
                        ugen,
                        calculation_rate=calculation_rate,
                        special_index=special_index,
                        **kwargs,
                    )
            ugens.append(ugen)
        variants_count, index = sdd._decode_int_16bit(value, index)
        synthdef = supriya.synthdefs.SynthDef(ugens=ugens, name=name, decompiled=True)
        if synthdef.name == synthdef.anonymous_name:
            synthdef._name = None
        return synthdef, index

    @staticmethod
    def _decode_string(value, index):
        length = struct.unpack(">B", value[index : index + 1])[0]
        index += 1
        result = value[index : index + length]
        result = result.decode("ascii")
        index += length
        return result, index

    @staticmethod
    def _decode_float(value, index):
        result = struct.unpack(">f", value[index : index + 4])[0]
        index += 4
        return result, index

    @staticmethod
    def _decode_int_8bit(value, index):
        result = struct.unpack(">B", value[index : index + 1])[0]
        index += 1
        return result, index

    @staticmethod
    def _decode_int_16bit(value, index):
        result = struct.unpack(">H", value[index : index + 2])[0]
        index += 2
        return result, index

    @staticmethod
    def _decode_int_32bit(value, index):
        result = struct.unpack(">I", value[index : index + 4])[0]
        index += 4
        return result, index

    @staticmethod
    def _collect_parameters_for_control(
        calculation_rate,
        indexed_parameters,
        inputs,
        output_count,
        starting_control_index,
        ugen_class,
    ):
        import supriya.synthdefs
        import supriya.ugens

        parameter_rate = ParameterRate.CONTROL
        if issubclass(ugen_class, supriya.synthdefs.TrigControl):
            parameter_rate = ParameterRate.TRIGGER
        elif calculation_rate == CalculationRate.SCALAR:
            parameter_rate = ParameterRate.SCALAR
        elif calculation_rate == CalculationRate.AUDIO:
            parameter_rate = ParameterRate.AUDIO
        parameters = []
        collected_output_count = 0
        lag = 0.0
        while collected_output_count < output_count:
            if inputs:
                lag = inputs[collected_output_count]
            parameter = indexed_parameters[
                starting_control_index + collected_output_count
            ]
            parameter._parameter_rate = parameter_rate
            if lag:
                parameter._lag = lag
            parameters.append(parameter)
            collected_output_count += len(parameter)
        return parameters

    ### PUBLIC METHODS ###

    @staticmethod
    def decompile_synthdef(value):
        synthdefs = SynthDefDecompiler.decompile_synthdefs(value)
        assert len(synthdefs) == 1
        return synthdefs[0]

    @staticmethod
    def decompile_synthdefs(value):
        synthdefs = []
        sdd = SynthDefDecompiler
        index = 4
        assert value[:index] == b"SCgf"
        file_version, index = sdd._decode_int_32bit(value, index)
        synthdef_count, index = sdd._decode_int_16bit(value, index)
        for _ in range(synthdef_count):
            synthdef, index = sdd._decompile_synthdef(value, index)
            synthdefs.append(synthdef)
        return synthdefs
