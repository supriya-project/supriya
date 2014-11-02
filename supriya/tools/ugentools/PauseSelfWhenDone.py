# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PauseSelfWhenDone(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        source=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of PauseSelfWhenDone.

        ::

            >>> source = ugentools.Line.kr()
            >>> pause_self_when_done = ugentools.PauseSelfWhenDone.ar(
            ...     source=source,
            ...     )
            >>> pause_self_when_done.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]