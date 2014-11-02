# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class FreeSelfWhenDone(UGen):
    r'''Free the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = ugentools.Line.kr()
        >>> free_self_when_done = ugentools.FreeSelfWhenDone.kr(
        ...     source=source,
        ...     )
        >>> free_self_when_done
        FreeSelfWhenDone.kr()

    '''

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
        assert source._has_done_action
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
        r'''Constructs a control-rate ugen.

        ::

            >>> source = ugentools.Line.kr()
            >>> free_self_when_done = ugentools.FreeSelfWhenDone.kr(
            ...     source=source,
            ...     )
            >>> free_self_when_done
            FreeSelfWhenDone.kr()

        Returns ugen graph.
        '''
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
        r'''Gets `source` input of FreeSelfWhenDone.

        ::

            >>> source = ugentools.Line.kr()
            >>> free_self_when_done = ugentools.FreeSelfWhenDone.kr(
            ...     source=source,
            ...     )
            >>> free_self_when_done.source
            OutputProxy(
                source=Line(
                    rate=<Rate.CONTROL: 1>,
                    done_action=0.0,
                    duration=1.0,
                    start=0.0,
                    stop=1.0
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]