# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Sum4(UGen):
    r'''Four-input summing unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> input_one = ugentools.SinOsc.ar()
        >>> input_two = ugentools.SinOsc.ar(phase=0.1)
        >>> input_three = ugentools.SinOsc.ar(phase=0.2)
        >>> input_four = ugentools.SinOsc.ar(phase=0.3)
        >>> ugentools.Sum4.new(
        ...     input_one=input_one,
        ...     input_two=input_two,
        ...     input_three=input_three,
        ...     input_four=input_four,
        ...     )
        Sum4.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

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
        Rate = synthdeftools.Rate
        inputs = [input_one, input_two, input_three, input_four]
        rate = Rate.from_collection(inputs)
        inputs.sort(
            key=lambda x: Rate.from_input(x),
            reverse=True,
            )
        inputs = tuple(inputs)
        UGen.__init__(
            self,
            rate=rate,
            input_one=input_one,
            input_two=input_two,
            input_three=input_three,
            input_four=input_four,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        input_one=None,
        input_two=None,
        input_three=None,
        input_four=None,
        **kwargs
        ):
        from supriya.tools import ugentools
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
        return ugen

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        input_one=None,
        input_two=None,
        input_three=None,
        input_four=None,
        ):
        ugen = cls._new_expanded(
            input_one=input_one,
            input_two=input_two,
            input_three=input_three,
            input_four=input_four,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def input_four(self):
        r'''Gets `input_four` input of Sum4.

        ::

            >>> input_four = None
            >>> sum_4 = ugentools.Sum4.ar(
            ...     input_four=input_four,
            ...     )
            >>> sum_4.input_four

        Returns input.
        '''
        index = self._ordered_input_names.index('input_four')
        return self._inputs[index]

    @property
    def input_one(self):
        r'''Gets `input_one` input of Sum4.

        ::

            >>> input_one = None
            >>> sum_4 = ugentools.Sum4.ar(
            ...     input_one=input_one,
            ...     )
            >>> sum_4.input_one

        Returns input.
        '''
        index = self._ordered_input_names.index('input_one')
        return self._inputs[index]

    @property
    def input_three(self):
        r'''Gets `input_three` input of Sum4.

        ::

            >>> input_three = None
            >>> sum_4 = ugentools.Sum4.ar(
            ...     input_three=input_three,
            ...     )
            >>> sum_4.input_three

        Returns input.
        '''
        index = self._ordered_input_names.index('input_three')
        return self._inputs[index]

    @property
    def input_two(self):
        r'''Gets `input_two` input of Sum4.

        ::

            >>> input_two = None
            >>> sum_4 = ugentools.Sum4.ar(
            ...     input_two=input_two,
            ...     )
            >>> sum_4.input_two

        Returns input.
        '''
        index = self._ordered_input_names.index('input_two')
        return self._inputs[index]