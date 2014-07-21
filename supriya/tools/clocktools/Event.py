# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Event(SupriyaObject):

    __slots__ = (
        '_payload',
        '_scheduled_time',
        )

    def __init__(
        self,
        scheduled_time=None,
        payload=None,
        ):
        self._payload = payload
        self._scheduled_time = scheduled_time

    def __call__(
        self,
        clock,
        current_time,
        ):
        print('ME:', abs(self._scheduled_time - current_time), self._payload)
        clock.schedule_absolutely(self._payload, self._scheduled_time + 3)

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        return self._payload

    @property
    def scheduled_time(self):
        return self._scheduled_time