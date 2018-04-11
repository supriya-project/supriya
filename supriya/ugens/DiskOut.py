import collections
from supriya.ugens.UGen import UGen


class DiskOut(UGen):
    """
    Records to a soundfile to disk.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
        >>> disk_out = supriya.ugens.DiskOut.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        >>> disk_out
        DiskOut.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Disk I/O UGens'

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        source=None,
        ):
        if not isinstance(source, collections.Sequence):
            source = (source,)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        source=None,
        ):
        """
        Constructs an audio-rate DiskOut.

        ::

            >>> buffer_id = 0
            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> disk_out = supriya.ugens.DiskOut.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> disk_out
            DiskOut.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        """
        Gets `buffer_id` input of DiskOut.

        ::

            >>> buffer_id = 0
            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> disk_out = supriya.ugens.DiskOut.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> disk_out.buffer_id
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of DiskOut.

        ::

            >>> buffer_id = 0
            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> disk_out = supriya.ugens.DiskOut.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> disk_out.source
            (SinOsc.ar()[0], SinOsc.ar()[0])

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return tuple(self._inputs[index:])
