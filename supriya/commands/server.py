import supriya.osc
from supriya.enums import RequestId

from .bases import Request, Response


class ClearScheduleRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.CLEAR_SCHEDULE

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        contents = [request_id]
        message = supriya.osc.OscMessage(*contents)
        return message


class DoneResponse(Response):

    ### INITIALIZER ###

    def __init__(self, action=None):
        self._action = action

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = osc_message.contents
        response = cls(action=tuple(arguments))
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def action(self):
        return self._action


class DumpOscRequest(Request):
    """
    A /dumpOSC request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.DumpOscRequest(1)
        >>> request
        DumpOscRequest(
            osc_status=1,
        )

    ::

        >>> request.to_osc()
        OscMessage('/dumpOSC', 1)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.DUMP_OSC

    ### INITIALIZER ###

    def __init__(self, osc_status=None):
        Request.__init__(self)
        self._osc_status = int(osc_status)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        osc_status = int(self.osc_status)
        assert 0 <= osc_status <= 4
        message = supriya.osc.OscMessage(request_id, osc_status)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def osc_status(self):
        return self._osc_status


class FailResponse(Response):

    ### INITIALIZER ###

    def __init__(self, failed_command=None, failure_reason=None):
        self._failed_command = failed_command
        self._failure_reason = failure_reason

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        failed_command = osc_message.contents[0]
        failure_reason = osc_message.contents[1:]
        if failure_reason:
            failure_reason = tuple(failure_reason)
        response = cls(failed_command=failed_command, failure_reason=failure_reason)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def failed_command(self):
        return self._failed_command

    @property
    def failure_reason(self):
        return self._failure_reason


class NothingRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.NOTHING

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        return supriya.osc.OscMessage(0)


class NotifyRequest(Request):
    """
    A /notify message.

    ::

        >>> import supriya.commands

        >>> request = supriya.commands.NotifyRequest(
        ...     notify_status=True,
        ... )
        >>> request
        NotifyRequest(
            notify_status=True,
        )

    ::

        >>> request.to_osc()
        OscMessage('/notify', 1)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.NOTIFY

    ### INITIALIZER ###

    def __init__(self, notify_status=None):
        Request.__init__(self)
        self._notify_status = bool(notify_status)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        notify_status = int(self.notify_status)
        message = supriya.osc.OscMessage(request_id, notify_status)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def notify_status(self):
        return self._notify_status

    @property
    def response_patterns(self):
        return ["/done", "/notify"], ["/fail", "/notify"]


class QuitRequest(Request):

    ### CLASS VARIABLES ###

    request_id = RequestId.QUIT

    ### INITIALIZER ###

    def __init__(self):
        Request.__init__(self)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        message = supriya.osc.OscMessage(request_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return ["/done", "/quit"], None


class StatusRequest(Request):
    """
    A /status request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.StatusRequest()
        >>> request
        StatusRequest()

    ::

        >>> request.to_osc()
        OscMessage('/status')

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.STATUS

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        message = supriya.osc.OscMessage(request_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return ["/status.reply"], None


class StatusResponse(Response):

    ### INITIALIZER ###

    def __init__(
        self,
        actual_sample_rate=None,
        average_cpu_usage=None,
        group_count=None,
        peak_cpu_usage=None,
        synth_count=None,
        synthdef_count=None,
        target_sample_rate=None,
        ugen_count=None,
    ):
        self._actual_sample_rate = actual_sample_rate
        self._average_cpu_usage = average_cpu_usage
        self._group_count = group_count
        self._peak_cpu_usage = peak_cpu_usage
        self._synth_count = synth_count
        self._synthdef_count = synthdef_count
        self._target_sample_rate = target_sample_rate
        self._ugen_count = ugen_count

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response from OSC message.

        ::

            >>> message = supriya.osc.OscMessage(
            ...     "/status.reply",
            ...     1,
            ...     0,
            ...     0,
            ...     2,
            ...     4,
            ...     0.040679048746824265,
            ...     0.15118031203746796,
            ...     44100.0,
            ...     44100.00077873274,
            ... )
            >>> supriya.commands.StatusResponse.from_osc_message(message)
            StatusResponse(
                actual_sample_rate=44100.00077873274,
                average_cpu_usage=0.040679048746824265,
                group_count=2,
                peak_cpu_usage=0.15118031203746796,
                synth_count=0,
                synthdef_count=4,
                target_sample_rate=44100.0,
                ugen_count=0,
            )

        """
        arguments = osc_message.contents[1:]
        (
            ugen_count,
            synth_count,
            group_count,
            synthdef_count,
            average_cpu_usage,
            peak_cpu_usage,
            target_sample_rate,
            actual_sample_rate,
        ) = arguments
        response = cls(
            actual_sample_rate=actual_sample_rate,
            average_cpu_usage=average_cpu_usage,
            group_count=group_count,
            peak_cpu_usage=peak_cpu_usage,
            synth_count=synth_count,
            synthdef_count=synthdef_count,
            target_sample_rate=target_sample_rate,
            ugen_count=ugen_count,
        )
        return response

    def to_dict(self):
        """
        Convert StatusResponse to JSON-serializable dictionay.

        ::

            >>> status_response = supriya.commands.StatusResponse(
            ...     actual_sample_rate=44100.05692801021,
            ...     average_cpu_usage=8.151924133300781,
            ...     group_count=6,
            ...     peak_cpu_usage=15.151398658752441,
            ...     synth_count=19,
            ...     synthdef_count=42,
            ...     target_sample_rate=44100.0,
            ...     ugen_count=685,
            ... )

        ::

            >>> import json
            >>> result = status_response.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(",", ": "),
            ...     sort_keys=True,
            ... )
            >>> print(result)
            {
                "server_status": {
                    "actual_sample_rate": 44100.05692801021,
                    "average_cpu_usage": 8.151924133300781,
                    "group_count": 6,
                    "peak_cpu_usage": 15.151398658752441,
                    "synth_count": 19,
                    "synthdef_count": 42,
                    "target_sample_rate": 44100.0,
                    "ugen_count": 685
                }
            }

        """
        result = {
            "server_status": {
                "actual_sample_rate": self.actual_sample_rate,
                "average_cpu_usage": self.average_cpu_usage,
                "group_count": self.group_count,
                "peak_cpu_usage": self.peak_cpu_usage,
                "synth_count": self.synth_count,
                "synthdef_count": self.synthdef_count,
                "target_sample_rate": self.target_sample_rate,
                "ugen_count": self.ugen_count,
            }
        }
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def actual_sample_rate(self):
        return self._actual_sample_rate

    @property
    def average_cpu_usage(self):
        return self._average_cpu_usage

    @property
    def group_count(self):
        return self._group_count

    @property
    def peak_cpu_usage(self):
        return self._peak_cpu_usage

    @property
    def synth_count(self):
        return self._synth_count

    @property
    def synthdef_count(self):
        return self._synthdef_count

    @property
    def target_sample_rate(self):
        return self._target_sample_rate

    @property
    def ugen_count(self):
        return self._ugen_count


class SyncedResponse(Response):

    ### INITIALIZER ###

    def __init__(self, sync_id=None):
        self._sync_id = sync_id

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = osc_message.contents
        response = cls(*arguments)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def sync_id(self):
        return self._sync_id


class SyncRequest(Request):
    """
    A /sync request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.SyncRequest(
        ...     sync_id=1999,
        ... )
        >>> request
        SyncRequest(
            sync_id=1999,
        )

    ::

        >>> request.to_osc()
        OscMessage('/sync', 1999)

    """

    ### CLASS VARIABLES ###

    request_id = RequestId.SYNC

    ### INITIALIZER ###

    def __init__(self, sync_id=None):
        Request.__init__(self)
        self._sync_id = int(sync_id)

    ### PUBLIC METHODS ###

    def to_osc(self, *, with_placeholders=False):
        request_id = self.request_name
        sync_id = int(self.sync_id)
        message = supriya.osc.OscMessage(request_id, sync_id)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def response_patterns(self):
        return ["/synced", self.sync_id], None

    @property
    def sync_id(self):
        return self._sync_id
