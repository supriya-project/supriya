# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Sum3(UGen):
    r'''Three-input summing unit generator.

    ::

        >>> from supriya.tools import synthdeftools
        >>> input_one = synthdeftools.SinOsc.ar()
        >>> input_two = synthdeftools.SinOsc.ar(phase=0.1)
        >>> input_three = synthdeftools.SinOsc.ar(phase=0.2)
        >>> synthdeftools.Sum3.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ...     )
        Sum3.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'input_one',
        'input_two',
        'input_three',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        input_one=None,
        input_two=None,
        input_three=None,
        ):
        from supriya.tools import synthdeftools
        Rate = synthdeftools.CalculationRate
        inputs = [input_one, input_two, input_three]
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
            )

    ### PRIVATE METHODS ###

    @classmethod
    def new(
        cls,
        input_one=None,
        input_two=None,
        input_three=None,
        ):
        kwargs = {
            'input_one': input_one,
            'input_two': input_two,
            'input_three': input_three,
            }
        ugens = []
        input_dicts = UGen.expand_dictionary(kwargs)
        for input_dict in input_dicts:
            input_one = input_dict['input_one']
            input_two = input_dict['input_two']
            input_three = input_dict['input_three']
            if input_three == 0:
                ugen = input_one + input_two
            elif input_two == 0:
                ugen = input_one + input_three
            elif input_one == 0:
                ugen = input_two + input_three
            else:
                ugen = cls(
                    input_one=input_one,
                    input_two=input_two,
                    input_three=input_three,
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdeftools.UGenArray(ugens)
