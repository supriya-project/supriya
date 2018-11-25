import collections
import struct

from supriya import utils
from supriya.system.SupriyaObject import SupriyaObject


class SynthDefDecompiler(SupriyaObject):
    """
    SynthDef decompiler.

    ::

        >>> import supriya.synthdefs
        >>> import supriya.ugens
        >>> with supriya.synthdefs.SynthDefBuilder(
        ...     frequency=440,
        ...     trigger=supriya.synthdefs.Parameter(
        ...         value=0.,
        ...         parameter_rate=supriya.synthdefs.ParameterRate.TRIGGER,
        ...         ),
        ...     ) as builder:
        ...     sin_osc = supriya.ugens.SinOsc.ar(frequency=builder['frequency'])
        ...     decay = supriya.ugens.Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder['trigger'],
        ...         )
        ...     enveloped_sin = sin_osc * decay
        ...     out = supriya.ugens.Out.ar(bus=0, source=enveloped_sin)
        ...
        >>> synthdef = builder.build()
        >>> graph(synthdef)  # doctest: +SKIP

    ::

        >>> print(synthdef)
        synthdef:
            name: 001520731aee5371fefab6b505cf64dd
            ugens:
            -   TrigControl.kr: null
            -   Decay.kr:
                    decay_time: 0.5
                    source: TrigControl.kr[0:trigger]
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
        >>> graph(decompiled_synthdef)  # doctest: +SKIP

    ::

        >>> print(decompiled_synthdef)
        synthdef:
            name: 001520731aee5371fefab6b505cf64dd
            ugens:
            -   TrigControl.kr: null
            -   Decay.kr:
                    decay_time: 0.5
                    source: TrigControl.kr[0:trigger]
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

    ### CLASS VARIABLES ###

    __documentation_section__ = "SynthDef Internals"

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
            ugen_class = getattr(supriya.ugens, ugen_name)
            ugen = supriya.ugens.UGen.__new__(ugen_class)
            if issubclass(ugen_class, supriya.ugens.Control):
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
                if issubclass(ugen_class, supriya.ugens.MultiOutUGen):
                    supriya.ugens.MultiOutUGen.__init__(
                        ugen,
                        calculation_rate=calculation_rate,
                        channel_count=output_count,
                        special_index=special_index,
                        **kwargs,
                    )
                else:
                    supriya.ugens.UGen.__init__(
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

        parameter_rate = supriya.synthdefs.ParameterRate.CONTROL
        if issubclass(ugen_class, supriya.ugens.TrigControl):
            parameter_rate = supriya.synthdefs.ParameterRate.TRIGGER
        elif calculation_rate == supriya.CalculationRate.SCALAR:
            parameter_rate = supriya.synthdefs.ParameterRate.SCALAR
        elif calculation_rate == supriya.CalculationRate.AUDIO:
            parameter_rate = supriya.synthdefs.ParameterRate.AUDIO
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
