# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Sum4(UGen):
    r'''Four-input summing unit generator.

    ::

        >>> from supriya.tools import synthdeftools
        >>> input_one = synthdeftools.SinOsc.ar()
        >>> input_two = synthdeftools.SinOsc.ar(phase=0.1)
        >>> input_three = synthdeftools.SinOsc.ar(phase=0.2)
        >>> input_four = synthdeftools.SinOsc.ar(phase=0.3)
        >>> synthdeftools.Sum4.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ...     input_four=input_four,
        ...     )
        Sum4.ar()

    '''
    
    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'input_one',
        'input_two',
        'input_three',
        'input_four',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        input_one=None,
        input_two=None,
        input_three=None,
        input_four=None,
        ):
        from supriya.tools import synthdeftools
        Rate = synthdeftools.CalculationRate
        inputs = [input_one, input_two, input_three, input_four]
        calculation_rate = Rate.from_collection(inputs)
        inputs.sort(
            key=lambda x: Rate.from_input(x),
            reverse=True,
            )
        inputs = tuple(inputs)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            input_one=input_one,
            input_two=input_two,
            input_three=input_three,
            input_four=input_four,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def new(
        cls,
        input_one=None,
        input_two=None,
        input_three=None,
        input_four=None,
        ):
        from supriya.tools import ugentools
        kwargs = {
            'input_one': input_one,
            'input_two': input_two,
            'input_three': input_three,
            'input_four': input_four,
            }
        ugens = []
        argument_dicts = UGen.expand_arguments(kwargs)
        for argument_dict in argument_dicts:
            input_one = argument_dict['input_one']    
            input_two = argument_dict['input_two']    
            input_three = argument_dict['input_three']    
            input_four = argument_dict['input_four']    
            if input_one == 0:
                ugen = ugentools.Sum3.new(
                    input_one=input_two,
                    input_two=input_three,
                    input_three=input_four,
                    )
            elif input_two == 0:
                ugen = ugentools.Sum3.new(
                    input_one=input_one,
                    input_two=input_three,
                    input_three=input_four,
                    )
            elif input_three == 0:
                ugen = ugentools.Sum3.new(
                    input_one=input_one,
                    input_two=input_two,
                    input_three=input_four,
                    )
            elif input_four == 0:
                ugen = ugentools.Sum3.new(
                    input_one=input_one,
                    input_two=input_two,
                    input_three=input_three,
                    )
            else:
                ugen = cls(
                    input_one=input_one,
                    input_two=input_two,
                    input_three=input_three,
                    input_four=input_four,
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdeftools.UGenArray(ugens)
