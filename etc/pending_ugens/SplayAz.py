import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class SplayAz(UGen):
    """

    ::

        >>> splay_az = supriya.ugens.SplayAz.ar(
        ...     center=0,
        ...     channel_count=4,
        ...     in_array=in_array,
        ...     level=1,
        ...     level_comp=True,
        ...     orientation=0.5,
        ...     spread=1,
        ...     width=2,
        ...     )
        >>> splay_az
        SplayAz.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'channel_count',
        'in_array',
        'spread',
        'level',
        'width',
        'center',
        'orientation',
        'level_comp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        center=0,
        channel_count=4,
        in_array=None,
        level=1,
        level_comp=True,
        orientation=0.5,
        spread=1,
        width=2,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            center=center,
            channel_count=channel_count,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            orientation=orientation,
            spread=spread,
            width=width,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        center=0,
        channel_count=4,
        in_array=None,
        level=1,
        level_comp=True,
        orientation=0.5,
        spread=1,
        width=2,
        ):
        """
        Constructs an audio-rate SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az
            SplayAz.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            channel_count=channel_count,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            orientation=orientation,
            spread=spread,
            width=width,
            )
        return ugen

    # def arFill(): ...

    @classmethod
    def kr(
        cls,
        center=0,
        channel_count=4,
        in_array=None,
        level=1,
        level_comp=True,
        orientation=0.5,
        spread=1,
        width=2,
        ):
        """
        Constructs a control-rate SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.kr(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az
            SplayAz.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            channel_count=channel_count,
            in_array=in_array,
            level=level,
            level_comp=level_comp,
            orientation=orientation,
            spread=spread,
            width=width,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def center(self):
        """
        Gets `center` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.center
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('center')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.channel_count
            4.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def in_array(self):
        """
        Gets `in_array` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.in_array

        Returns ugen input.
        """
        index = self._ordered_input_names.index('in_array')
        return self._inputs[index]

    @property
    def level(self):
        """
        Gets `level` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.level
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def level_comp(self):
        """
        Gets `level_comp` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.level_comp
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level_comp')
        return self._inputs[index]

    @property
    def orientation(self):
        """
        Gets `orientation` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.orientation
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('orientation')
        return self._inputs[index]

    @property
    def spread(self):
        """
        Gets `spread` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.spread
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('spread')
        return self._inputs[index]

    @property
    def width(self):
        """
        Gets `width` input of SplayAz.

        ::

            >>> splay_az = supriya.ugens.SplayAz.ar(
            ...     center=0,
            ...     channel_count=4,
            ...     in_array=in_array,
            ...     level=1,
            ...     level_comp=True,
            ...     orientation=0.5,
            ...     spread=1,
            ...     width=2,
            ...     )
            >>> splay_az.width
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('width')
        return self._inputs[index]
