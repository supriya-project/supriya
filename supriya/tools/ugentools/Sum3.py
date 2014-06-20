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
    def _new_single(
        cls,
        input_one=None,
        input_two=None,
        input_three=None,
        **kwargs
        ):
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
        return ugen

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        input_one=None,
        input_two=None,
        input_three=None,
        ):
        ugen = cls._new_expanded(
            input_one=input_one,
            input_two=input_two,
            input_three=input_three,
            )
        return ugen
