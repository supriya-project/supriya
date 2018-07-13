import collections
from supriya import utils
import supriya.osc
from supriya.commands.Request import Request


class BufferGenerateRequest(Request):
    """
    A /b_gen request.

    This requests models the 'cheby', 'sine1', 'sine2' and 'sine3' /b_gen
    commands.

    Use BufferCopyRequest for `/b_gen copy` and BufferNormalizeRequest for
    `/b_gen normalize` and `/b_gen wnormalize`.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferGenerateRequest(
        ...     amplitudes=(1., 0.5, 0.25),
        ...     as_wavetable=True,
        ...     buffer_id=23,
        ...     command_name='sine3',
        ...     frequencies=(1, 2, 3),
        ...     phases=(0, 0.5, 0),
        ...     should_clear_first=True,
        ...     should_normalize=True,
        ...     )
        >>> print(request)
        BufferGenerateRequest(
            amplitudes=(1.0, 0.5, 0.25),
            as_wavetable=True,
            buffer_id=23,
            command_name='sine3',
            frequencies=(1.0, 2.0, 3.0),
            phases=(0.0, 0.5, 0.0),
            should_clear_first=True,
            should_normalize=True,
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(38, 23, 'sine3', 7, 1.0, 1.0, 0.0, 0.5, 2.0, 0.5, 0.25, 3.0, 0.0)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_GENERATE
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_amplitudes',
        '_as_wavetable',
        '_buffer_id',
        '_command_name',
        '_frequencies',
        '_phases',
        '_should_clear_first',
        '_should_normalize',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        amplitudes=None,
        as_wavetable=None,
        buffer_id=None,
        command_name=None,
        frequencies=None,
        phases=None,
        should_clear_first=None,
        should_normalize=None,
    ):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        assert command_name in (
            'cheby',
            'sine1',
            'sine2',
            'sine3',
            )
        self._command_name = command_name
        if as_wavetable is not None:
            as_wavetable = bool(as_wavetable)
        self._as_wavetable = as_wavetable
        if should_clear_first is not None:
            should_clear_first = bool(should_clear_first)
        self._should_clear_first = should_clear_first
        if should_normalize is not None:
            should_normalize = bool(should_normalize)
        self._should_normalize = should_normalize
        self._frequencies = None
        self._phases = None
        if command_name in ('cheby', 'sine1'):
            if not isinstance(amplitudes, collections.Sequence):
                amplitudes = (amplitudes,)
            amplitudes = tuple(float(_) for _ in amplitudes)
            assert len(amplitudes)
            self._amplitudes = amplitudes
        if command_name == 'sine2':
            amplitudes = tuple(float(_) for _ in amplitudes)
            frequencies = tuple(float(_) for _ in frequencies)
            assert 0 < len(amplitudes)
            assert len(amplitudes) == len(frequencies)
            self._amplitudes = amplitudes
            self._frequencies = frequencies
        if command_name == 'sine3':
            amplitudes = tuple(float(_) for _ in amplitudes)
            frequencies = tuple(float(_) for _ in frequencies)
            phases = tuple(float(_) for _ in phases)
            assert 0 < len(amplitudes)
            assert len(amplitudes) == len(frequencies) == len(phases)
            self._amplitudes = amplitudes
            self._frequencies = frequencies
            self._phases = phases

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [
            request_id,
            buffer_id,
            self.command_name,
            self.flags,
            ]
        if self.command_name in (
            'cheby',
            'sine1',
        ):
            coefficients = self.amplitudes
        elif self.command_name == 'sine2':
            coefficients = zip(
                self.amplitudes,
                self.frequencies,
                )
            coefficients = tuple(coefficients)
        elif self.command_name == 'sine3':
            coefficients = zip(
                self.amplitudes,
                self.frequencies,
                self.phases,
                )
            coefficients = tuple(coefficients)
        coefficients = utils.flatten_iterable(coefficients)
        contents.extend(coefficients)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC METHODS ###

    @classmethod
    def chebyshev(
        cls,
        amplitudes=None,
        as_wavetable=True,
        buffer_id=None,
        should_normalize=True,
        should_clear_first=True,
        ):
        command_name = 'cheby'
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
            )
        return request

    @classmethod
    def sine1(
        cls,
        amplitudes=None,
        as_wavetable=True,
        buffer_id=None,
        should_normalize=True,
        should_clear_first=True,
        ):
        command_name = 'sine1'
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
            )
        return request

    @classmethod
    def sine2(
        cls,
        amplitudes=None,
        as_wavetable=True,
        buffer_id=None,
        frequencies=None,
        should_normalize=True,
        should_clear_first=True,
        ):
        command_name = 'sine2'
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            frequencies=frequencies,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
            )
        return request

    @classmethod
    def sine3(
        cls,
        amplitudes=None,
        as_wavetable=True,
        buffer_id=None,
        frequencies=None,
        phases=None,
        should_normalize=True,
        should_clear_first=True,
        ):
        command_name = 'sine3'
        request = cls(
            amplitudes=amplitudes,
            as_wavetable=as_wavetable,
            buffer_id=buffer_id,
            command_name=command_name,
            frequencies=frequencies,
            phases=phases,
            should_clear_first=should_clear_first,
            should_normalize=should_normalize,
            )
        return request

    ### PUBLIC PROPERTIES ###

    @property
    def amplitudes(self):
        return self._amplitudes

    @property
    def as_wavetable(self):
        return self._as_wavetable

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def command_name(self):
        return self._command_name

    @property
    def flags(self):
        flags = sum((
            1 * int(bool(self.should_normalize)),
            2 * int(bool(self.as_wavetable)),
            4 * int(bool(self.should_clear_first)),
            ))
        return flags

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def phases(self):
        return self._phases

    @property
    def response_patterns(self):
        return [['/done', '/b_gen', self.buffer_id]]

    @property
    def response_specification(self):
        import supriya.commands
        return {
            supriya.commands.DoneResponse: {
                'action': ('/b_gen', self.buffer_id),
                },
            }

    @property
    def request_id(self):
        import supriya.commands
        return supriya.commands.RequestId.BUFFER_GENERATE

    @property
    def should_clear_first(self):
        return self._should_clear_first

    @property
    def should_normalize(self):
        return self._should_normalize
