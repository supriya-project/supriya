# -*- encoding: utf-8 -*-
from __future__ import print_function
import struct
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefDecompiler(SupriyaObject):
    r'''

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> builder = synthdeftools.SynthDefBuilder()
        >>> builder.add_parameter('frequency', 440)
        >>> builder.add_parameter(
        ...     'trigger', 0, synthdeftools.ParameterRate.TRIGGER,
        ...     )
        >>> with builder:
        ...     sin_osc = ugentools.SinOsc.ar(frequency=builder['frequency'])
        ...     decay = ugentools.Decay.kr(
        ...         decay_time=0.5,
        ...         source=builder['trigger'],
        ...         )
        ...     enveloped_sin = sin_osc * decay
        ...     out = ugentools.Out.ar(bus=0, source=enveloped_sin)
        ...
        >>> synthdef = builder.build()
        >>> print(synthdef)
        SynthDef 001520731aee5371fefab6b505cf64dd {
            0_TrigControl[0] -> 1_Decay[0:source]
            const_0:0.5 -> 1_Decay[1:decay_time]
            2_Control[0] -> 3_SinOsc[0:frequency]
            const_1:0.0 -> 3_SinOsc[1:phase]
            3_SinOsc[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            1_Decay[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            const_1:0.0 -> 5_Out[0:bus]
            4_BinaryOpUGen:MULTIPLICATION[0] -> 5_Out[1:source]
        }

    ::

        >>> compiled_synthdef = synthdef.compile()
        >>> sdd = synthdeftools.SynthDefDecompiler
        >>> decompiled_synthdef = sdd.decompile_synthdefs(compiled_synthdef)[0]
        >>> print(decompiled_synthdef)
        SynthDef 001520731aee5371fefab6b505cf64dd {
            0_TrigControl[0] -> 1_Decay[0:source]
            const_0:0.5 -> 1_Decay[1:decay_time]
            2_Control[0] -> 3_SinOsc[0:frequency]
            const_1:0.0 -> 3_SinOsc[1:phase]
            3_SinOsc[0] -> 4_BinaryOpUGen:MULTIPLICATION[0:left]
            1_Decay[0] -> 4_BinaryOpUGen:MULTIPLICATION[1:right]
            const_1:0.0 -> 5_Out[0:bus]
            4_BinaryOpUGen:MULTIPLICATION[0] -> 5_Out[1:source]
        }

    ::

        >>> str(synthdef) == str(decompiled_synthdef)
        True

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    ### PUBLIC METHODS ###

    @staticmethod
    def decompile_synthdefs(value):
        synthdefs = []
        sdd = SynthDefDecompiler
        index = 4
        assert value[:index] == 'SCgf'
        file_version, index = sdd.decode_int_32bit(value, index)
        synthdef_count, index = sdd.decode_int_16bit(value, index)
        for _ in range(synthdef_count):
            synthdef, index = sdd.decompile_synthdef(value, index)
            synthdefs.append(synthdef)
        return synthdefs

    @staticmethod
    def decode_constants(value, index):
        sdd = SynthDefDecompiler
        constants = []
        constants_count, index = sdd.decode_int_32bit(value, index)
        for _ in range(constants_count):
            constant, index = sdd.decode_float(value, index)
            constants.append(constant)
        return constants, index

    @staticmethod
    def decode_parameters(value, index):
        sdd = SynthDefDecompiler
        parameter_values = []
        parameter_count, index = sdd.decode_int_32bit(value, index)
        for _ in range(parameter_count):
            parameter_value, index = sdd.decode_float(value, index)
            parameter_values.append(parameter_value)
        parameter_count, index = sdd.decode_int_32bit(value, index)
        parameter_names = [None] * parameter_count
        for _ in range(parameter_count):
            parameter_name, index = sdd.decode_string(value, index)
            parameter_index, index = sdd.decode_int_32bit(value, index)
            parameter_names[parameter_index] = parameter_name
        return parameter_names, parameter_values, index

    @staticmethod
    def decompile_synthdef(value, index):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        sdd = SynthDefDecompiler
        synthdef = None
        name, index = sdd.decode_string(value, index)
        constants, index = sdd.decode_constants(value, index)
        parameter_names, parameter_values, index = \
            sdd.decode_parameters(value, index)
        ugens = []
        ugen_count, index = sdd.decode_int_32bit(value, index)
        for i in range(ugen_count):
            ugen_name, index = sdd.decode_string(value, index)
            calculation_rate, index = sdd.decode_int_8bit(value, index)
            calculation_rate = synthdeftools.CalculationRate(calculation_rate)
            input_count, index = sdd.decode_int_32bit(value, index)
            output_count, index = sdd.decode_int_32bit(value, index)
            special_index, index = sdd.decode_int_16bit(value, index)
            inputs = []
            for _ in range(input_count):
                ugen_index, index = sdd.decode_int_32bit(value, index)
                if ugen_index == 0xffffffff:
                    constant_index, index = sdd.decode_int_32bit(value, index)
                    constant_index = int(constant_index)
                    inputs.append(constants[constant_index])
                else:
                    ugen = ugens[ugen_index]
                    ugen_output_index, index = sdd.decode_int_32bit(value, index)
                    output_proxy = ugen[ugen_output_index]
                    inputs.append(output_proxy)
            for _ in range(output_count):
                output_rate, index = sdd.decode_int_8bit(value, index)
            ugen_class = getattr(ugentools, ugen_name)
            ugen = synthdeftools.UGen.__new__(ugen_class)
            if issubclass(ugen_class, ugentools.Control):
                starting_control_index = special_index
                control_names = parameter_names[
                    starting_control_index:
                    starting_control_index + output_count
                    ]
                ugentools.Control.__init__(
                    ugen,
                    control_names=control_names,
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
                if issubclass(ugen_class, ugentools.MultiOutUGen):
                    ugentools.MultiOutUGen.__init__(
                        ugen,
                        calculation_rate=calculation_rate,
                        channel_count=output_count,
                        special_index=special_index,
                        **kwargs
                        )
                else:
                    synthdeftools.UGen.__init__(
                        ugen,
                        calculation_rate=calculation_rate,
                        special_index=special_index,
                        **kwargs
                        )
            ugens.append(ugen)
        variants_count, index = sdd.decode_int_16bit(value, index)
        synthdef = synthdeftools.SynthDef(
            ugens=ugens,
            name=name,
            )
        return synthdef, index

    @staticmethod
    def decode_string(value, index):
        length = struct.unpack('>B', value[index:index + 1])[0]
        index += 1
        result = str(value[index:index + length])
        index += length
        return result, index

    @staticmethod
    def decode_float(value, index):
        result = struct.unpack('>f', value[index:index + 4])[0]
        index += 4
        return result, index

    @staticmethod
    def decode_int_8bit(value, index):
        result = struct.unpack('>B', value[index:index + 1])[0]
        index += 1
        return result, index

    @staticmethod
    def decode_int_16bit(value, index):
        result = struct.unpack('>H', value[index:index + 2])[0]
        index += 2
        return result, index

    @staticmethod
    def decode_int_32bit(value, index):
        result = struct.unpack('>I', value[index:index + 4])[0]
        index += 4
        return result, index