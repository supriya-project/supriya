# -*- encoding: utf-8 -*-
from supriya.tools.responsetools.Response import Response


class StatusResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_actual_sample_rate',
        '_average_cpu_usage',
        '_group_count',
        '_peak_cpu_usage',
        '_synth_count',
        '_synthdef_count',
        '_target_sample_rate',
        '_ugen_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        actual_sample_rate=None,
        average_cpu_usage=None,
        group_count=None,
        osc_message=None,
        peak_cpu_usage=None,
        synth_count=None,
        synthdef_count=None,
        target_sample_rate=None,
        ugen_count=None,
        ):
        Response.__init__(
            self,
            osc_message=osc_message,
            )
        self._actual_sample_rate = actual_sample_rate
        self._average_cpu_usage = average_cpu_usage
        self._group_count = group_count
        self._peak_cpu_usage = peak_cpu_usage
        self._synth_count = synth_count
        self._synthdef_count = synthdef_count
        self._target_sample_rate = target_sample_rate
        self._ugen_count = ugen_count

    ### PUBLIC METHODS ###

    def to_dict(self):
        """
        Convert StatusResponse to JSON-serializable dictionay.

        ::

            >>> status_response = responsetools.StatusResponse(
            ...     actual_sample_rate=44100.05692801021,
            ...     average_cpu_usage=8.151924133300781,
            ...     group_count=6,
            ...     peak_cpu_usage=15.151398658752441,
            ...     synth_count=19,
            ...     synthdef_count=42,
            ...     target_sample_rate=44100.0,
            ...     ugen_count=685
            ...     )

        ::

            >>> import json
            >>> result = status_response.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(',', ': '),
            ...     sort_keys=True,
            ...     )
            >>> print(result)
            {
                "status": {
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
            'status': {
                'actual_sample_rate': self.actual_sample_rate,
                'average_cpu_usage': self.average_cpu_usage,
                'group_count': self.group_count,
                'peak_cpu_usage': self.peak_cpu_usage,
                'synth_count': self.synth_count,
                'synthdef_count': self.synthdef_count,
                'target_sample_rate': self.target_sample_rate,
                'ugen_count': self.ugen_count,
                },
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
