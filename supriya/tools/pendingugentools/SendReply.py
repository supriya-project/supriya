# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.SendTrig import SendTrig


class SendReply(SendTrig):
    """

    ::

        >>> send_reply = ugentools.SendReply.ar(
        ...     cmd_name='/reply',
        ...     reply_id=-1,
        ...     trigger=0,
        ...     values=values,
        ...     )
        >>> send_reply
        SendReply.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'cmd_name',
        'values',
        'reply_id',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        cmd_name='/reply',
        reply_id=-1,
        trigger=0,
        values=None,
        ):
        SendTrig.__init__(
            self,
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            reply_id=reply_id,
            trigger=trigger,
            values=values,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        cmd_name='/reply',
        reply_id=-1,
        trigger=0,
        values=None,
        ):
        """
        Constructs an audio-rate SendReply.

        ::

            >>> send_reply = ugentools.SendReply.ar(
            ...     cmd_name='/reply',
            ...     reply_id=-1,
            ...     trigger=0,
            ...     values=values,
            ...     )
            >>> send_reply
            SendReply.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            reply_id=reply_id,
            trigger=trigger,
            values=values,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        cmd_name='/reply',
        reply_id=-1,
        trigger=0,
        values=None,
        ):
        """
        Constructs a control-rate SendReply.

        ::

            >>> send_reply = ugentools.SendReply.kr(
            ...     cmd_name='/reply',
            ...     reply_id=-1,
            ...     trigger=0,
            ...     values=values,
            ...     )
            >>> send_reply
            SendReply.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            cmd_name=cmd_name,
            reply_id=reply_id,
            trigger=trigger,
            values=values,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def cmd_name(self):
        """
        Gets `cmd_name` input of SendReply.

        ::

            >>> send_reply = ugentools.SendReply.ar(
            ...     cmd_name='/reply',
            ...     reply_id=-1,
            ...     trigger=0,
            ...     values=values,
            ...     )
            >>> send_reply.cmd_name

        Returns ugen input.
        """
        index = self._ordered_input_names.index('cmd_name')
        return self._inputs[index]

    @property
    def reply_id(self):
        """
        Gets `reply_id` input of SendReply.

        ::

            >>> send_reply = ugentools.SendReply.ar(
            ...     cmd_name='/reply',
            ...     reply_id=-1,
            ...     trigger=0,
            ...     values=values,
            ...     )
            >>> send_reply.reply_id
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('reply_id')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of SendReply.

        ::

            >>> send_reply = ugentools.SendReply.ar(
            ...     cmd_name='/reply',
            ...     reply_id=-1,
            ...     trigger=0,
            ...     values=values,
            ...     )
            >>> send_reply.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def values(self):
        """
        Gets `values` input of SendReply.

        ::

            >>> send_reply = ugentools.SendReply.ar(
            ...     cmd_name='/reply',
            ...     reply_id=-1,
            ...     trigger=0,
            ...     values=values,
            ...     )
            >>> send_reply.values

        Returns ugen input.
        """
        index = self._ordered_input_names.index('values')
        return self._inputs[index]
