# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class StatusResponse(SupriyaValueObject):

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
        ugen_count=None,
        synth_count=None,
        group_count=None,
        synthdef_count=None,
        average_cpu_usage=None,
        peak_cpu_usage=None,
        target_sample_rate=None,
        actual_sample_rate=None,
        ):
        self._actual_sample_rate = actual_sample_rate
        self._average_cpu_usage = average_cpu_usage
        self._group_count = group_count
        self._peak_cpu_usage = peak_cpu_usage
        self._synth_count = synth_count
        self._synthdef_count = synthdef_count
        self._target_sample_rate = target_sample_rate
        self._ugen_count = ugen_count

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
