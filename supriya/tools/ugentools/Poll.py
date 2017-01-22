# -*- encoding: utf-8 -*-
from __future__ import print_function
import collections
from supriya.tools.ugentools.UGen import UGen


class Poll(UGen):
    """
    A UGen poller.

    ::

        >>> sine = ugentools.SinOsc.ar()
        >>> trigger = ugentools.Impulse.kr(1)
        >>> poll = ugentools.Poll.ar(
        ...     source=sine,
        ...     trigger=trigger,
        ...     trigger_id=1234,
        ...     )
        >>> poll
        Poll.ar()

    ..  container:: example

        Unlike **sclang**, Python does not share any inter-process
        communication with **scsynth**. This means that the Poll UGen is not
        able to automatically print out its diagnostic messages into a Python
        interpreter session.

        To get information out of the Poll UGen, we first need to set the
        Poll's `trigger_id` to a value greater than 0. This will cause the poll
        to send `/tr` OSC messages back to its client - Python. We can then
        register a callback to respond to these `/tr` messages.

        ::

            >>> from __future__ import print_function
            >>> from supriya import *

        ::

            >>> with SynthDefBuilder() as builder:
            ...     sine = ugentools.SinOsc.ar()
            ...     trigger = ugentools.Impulse.kr(1)
            ...     poll = ugentools.Poll.ar(
            ...         source=sine,
            ...         trigger=trigger,
            ...         trigger_id=1234,
            ...         )
            ...
            >>> synthdef = builder.build()

        ::

            >>> server = Server().boot()
            >>> synth = Synth(synthdef).allocate()
            >>> response_callback = responsetools.ResponseCallback(
            ...     prototype=responsetools.TriggerResponse,
            ...     procedure=lambda response: print(
            ...         'Poll value is: {}'.format(response.trigger_value)),
            ...     )
            >>> server.register_response_callback(response_callback)

        ::

            >>> server.quit()
            <Server: offline>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'source',
        'trigger_id',
        )

    _unexpanded_argument_names = None

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        label=None,
        source=None,
        trigger=None,
        trigger_id=-1,
        ):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        if label is None:
            if isinstance(source, ugentools.UGen):
                label = type(source).__name__
            elif isinstance(source, synthdeftools.OutputProxy):
                label = type(source.source).__name__
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
            )
        label = str(label)
        self._configure_input('label', len(label))
        for character in label:
            self._configure_input('label', ord(character))

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        label=None,
        source=None,
        trigger=None,
        trigger_id=-1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        label=None,
        source=None,
        trigger=None,
        trigger_id=-1,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
            )
        return ugen

    @classmethod
    def new(
        cls,
        label=None,
        source=None,
        trigger=None,
        trigger_id=-1,
        ):
        from supriya.tools import synthdeftools
        if isinstance(source, collections.Sequence):
            source = (source,)
        calculation_rates = []
        for single_source in source:
            rate = synthdeftools.CalculationRate.from_input(single_source)
            calculation_rates.append(rate)
        ugen = cls._new_expanded(
            calculation_rate=calculation_rates,
            label=label,
            source=source,
            trigger=trigger,
            trigger_id=trigger_id,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def label(self):
        """
        Gets `label` input of Poll.

        ::

            >>> sine = ugentools.SinOsc.ar()
            >>> trigger = ugentools.Impulse.kr(1)
            >>> poll = ugentools.Poll.ar(
            ...     label='Foo',
            ...     source=sine,
            ...     trigger=trigger,
            ...     trigger_id=1234,
            ...     )
            >>> poll.label
            'Foo'

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger_id') + 2
        characters = self._inputs[index:]
        characters = [chr(int(_)) for _ in characters]
        label = ''.join(characters)
        return label

    @property
    def source(self):
        """
        Gets `source` input of Poll.

        ::

            >>> sine = ugentools.SinOsc.ar()
            >>> trigger = ugentools.Impulse.kr(1)
            >>> poll = ugentools.Poll.ar(
            ...     label='Foo',
            ...     source=sine,
            ...     trigger=trigger,
            ...     trigger_id=1234,
            ...     )
            >>> poll.source
            OutputProxy(
                source=SinOsc(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Poll.

        ::

            >>> sine = ugentools.SinOsc.ar()
            >>> trigger = ugentools.Impulse.kr(1)
            >>> poll = ugentools.Poll.ar(
            ...     label='Foo',
            ...     source=sine,
            ...     trigger=trigger,
            ...     trigger_id=1234,
            ...     )
            >>> poll.trigger
            OutputProxy(
                source=Impulse(
                    calculation_rate=CalculationRate.CONTROL,
                    frequency=1.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def trigger_id(self):
        """
        Gets `trigger_id` input of Poll.

        ::

            >>> sine = ugentools.SinOsc.ar()
            >>> trigger = ugentools.Impulse.kr(1)
            >>> poll = ugentools.Poll.ar(
            ...     label='Foo',
            ...     source=sine,
            ...     trigger=trigger,
            ...     trigger_id=1234,
            ...     )
            >>> poll.trigger_id
            1234.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger_id')
        return self._inputs[index]
