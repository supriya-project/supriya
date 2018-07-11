import collections
from supriya.ugens.UGen import UGen


class Poll(UGen):
    """
    A UGen poller.

    ::

        >>> sine = supriya.ugens.SinOsc.ar()
        >>> trigger = supriya.ugens.Impulse.kr(1)
        >>> poll = supriya.ugens.Poll.ar(
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

            >>> with SynthDefBuilder() as builder:
            ...     sine = supriya.ugens.SinOsc.ar()
            ...     trigger = supriya.ugens.Impulse.kr(1)
            ...     poll = supriya.ugens.Poll.ar(
            ...         source=sine,
            ...         trigger=trigger,
            ...         trigger_id=1234,
            ...         )
            ...
            >>> synthdef = builder.build()

        ::

            >>> server = Server().boot()
            >>> synth = Synth(synthdef).allocate()
            >>> callback = server.osc_io.register(
            ...     pattern='/tr',
            ...     procedure=lambda response: print(
            ...         'Poll value is: {}'.format(response.value)),
            ...     once=True,
            ...     parse_response=True,
            ...     )

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
        import supriya.synthdefs
        import supriya.ugens
        if label is None:
            if isinstance(source, supriya.ugens.UGen):
                label = type(source).__name__
            elif isinstance(source, supriya.synthdefs.OutputProxy):
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
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
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
        import supriya.synthdefs
        if isinstance(source, collections.Sequence):
            source = (source,)
        calculation_rates = []
        for single_source in source:
            rate = supriya.synthdefs.CalculationRate.from_input(single_source)
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

            >>> sine = supriya.ugens.SinOsc.ar()
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> poll = supriya.ugens.Poll.ar(
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

            >>> sine = supriya.ugens.SinOsc.ar()
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> poll = supriya.ugens.Poll.ar(
            ...     label='Foo',
            ...     source=sine,
            ...     trigger=trigger,
            ...     trigger_id=1234,
            ...     )
            >>> poll.source
            SinOsc.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of Poll.

        ::

            >>> sine = supriya.ugens.SinOsc.ar()
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> poll = supriya.ugens.Poll.ar(
            ...     label='Foo',
            ...     source=sine,
            ...     trigger=trigger,
            ...     trigger_id=1234,
            ...     )
            >>> poll.trigger
            Impulse.kr()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def trigger_id(self):
        """
        Gets `trigger_id` input of Poll.

        ::

            >>> sine = supriya.ugens.SinOsc.ar()
            >>> trigger = supriya.ugens.Impulse.kr(1)
            >>> poll = supriya.ugens.Poll.ar(
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
