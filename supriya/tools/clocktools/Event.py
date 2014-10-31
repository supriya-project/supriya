# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Event(SupriyaObject):
    r'''An event.

    ::

        >>> event = clocktools.Event(
        ...     payload={
        ...         'foo': 1,
        ...         'bar': 2,
        ...         },
        ...      scheduled_time=0.5,
        ...      )
        >>> print(format(event))
        supriya.tools.clocktools.Event(
            scheduled_time=0.5,
            payload={
                'bar': 2,
                'foo': 1,
                },
            )

    '''

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
        r'''Schedules event on `clock`.

        Returns none.
        '''
        print('ME:', abs(self._scheduled_time - current_time), self._payload)
        clock.schedule_absolutely(self._payload, self._scheduled_time + 3)

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        r'''Gets the event's payload.

        Returns object.
        '''
        return self._payload

    @property
    def scheduled_time(self):
        r'''Gets event's scheduled time.

        Returns float.
        '''
        return self._scheduled_time