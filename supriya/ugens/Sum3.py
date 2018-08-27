import collections
from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class Sum3(UGen):
    """
    A three-input summing unit generator.

    ::

        >>> input_one = supriya.ugens.SinOsc.ar()
        >>> input_two = supriya.ugens.SinOsc.ar(phase=0.1)
        >>> input_three = supriya.ugens.SinOsc.ar(phase=0.2)
        >>> supriya.ugens.Sum3.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ...     )
        Sum3.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    _ordered_input_names = collections.OrderedDict([
        ('input_one', None),
        ('input_two', None),
        ('input_three', None),
    ])

    _valid_calculation_rates = ()

    ### INITIALIZER ###

    def __init__(
        self,
        input_one=None,
        input_two=None,
        input_three=None,
    ):
        inputs = [input_one, input_two, input_three]
        calculation_rate = CalculationRate.from_expr(inputs)
        inputs.sort(
            key=lambda x: CalculationRate.from_expr(x),
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
