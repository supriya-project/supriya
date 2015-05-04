# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Control(MultiOutUGen):
    r'''A control-rate control ugen.

    Control ugens can be set and routed externally to interact with a running
    synth. Controls are created from the parameters of a synthesizer
    definition, and typically do not need to be created by hand.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'UGen Internals'

    __slots__ = (
        '_channel_count',
        '_control_names',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        control_names,
        calculation_rate=None,
        starting_control_index=0,
        ):
        from supriya.tools import synthdeftools
        names = []
        for x in control_names:
            if not isinstance(x, synthdeftools.Parameter):
                x = synthdeftools.Parameter(name=x, value=0)
            names.append(x)
        names.sort(key=lambda x: x.name)
        self._control_names = tuple(names)
        MultiOutUGen.__init__(
            self,
            channel_count=len(control_names),
            calculation_rate=calculation_rate,
            special_index=starting_control_index,
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        r'''Gets output proxy at `i`, via index or control name.

        Returns output proxy.
        '''
        from supriya import synthdeftools
        if type(i) == int:
            if len(self.control_names) == 1:
                return synthdeftools.OutputProxy(self, 0)
            return synthdeftools.OutputProxy(self, i)
        else:
            return self[self._get_control_index(i)]

    def __len__(self):
        r'''Gets number of ugen outputs.

        Equal to the number of control names.

        Returns integer.
        '''
        return len(self.control_names)

    ### PRIVATE METHODS ###

    def _get_control_index(self, control_name):
        for i, parameter in enumerate(self._control_names):
            if parameter.name == control_name:
                return i
        raise ValueError

    def _get_outputs(self):
        return [self.calculation_rate] * len(self)

    ### PUBLIC PROPERTIES ###

    @property
    def control_names(self):
        r'''Gets control names associated with control.

        Returns tuple.
        '''
        return self._control_names

    @property
    def controls(self):
        r'''Gets controls of control ugen.

        Returns ugen graph.
        '''
        from supriya import synthdeftools
        if len(self.control_names) == 1:
            result = self
        else:
            result = [
                synthdeftools.OutputProxy(self, i)
                for i in range(len(self.control_names))
                ]
        return result

    @property
    def starting_control_index(self):
        r'''Gets starting control index of control ugen.

        Equivalent to the control ugen's special index.

        Returns integer.
        '''
        return self._special_index