import functools
import threading
from supriya.system.SupriyaObject import SupriyaObject
from typing import Callable, Dict, Set


class PubSub(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    _lock = threading.Lock()
    _subscribers: Dict[Callable, Set[str]] = {}
    _topics: Dict[str, Set[Callable]] = {}

    ### PRIVATE METHODS ###

    @classmethod
    def _unsubscribe(cls, subscriber, topic):
        if topic not in cls._topics:
            return
        subscribers = cls._topics[topic]
        if subscriber in subscribers:
            subscribers.remove(subscriber)
        if not subscribers:
            del (cls._topics[topic])
        topics = cls._subscribers[subscriber]
        if topic in topics:
            topics.remove(topic)
        if not topics:
            del (cls._subscribers[subscriber])

    ### PUBLIC METHODS ###

    @classmethod
    def clear(cls):
        with cls._lock:
            cls._subscriptions = {}
            cls._topics = {}

    @classmethod
    def notify(cls, topic, event=None):
        with cls._lock:
            subscribers = cls._topics.get(topic, set()).copy()
        for subscriber in subscribers:
            subscriber.notify(topic, event)

    @classmethod
    def subscribe(cls, subscriber, topic):
        with cls._lock:
            cls._subscribers.setdefault(subscriber, set()).add(topic)
            cls._topics.setdefault(topic, set()).add(subscriber)

    @classmethod
    def unsubscribe(cls, subscriber, topic):
        with cls._lock:
            cls._unsubscribe(subscriber, topic)

    @classmethod
    def unsubscribe_all(cls, subscriber):
        with cls._lock:
            if subscriber not in cls._subscribers:
                return
            topics = cls._subscribers[subscriber]
            for topic in topics.copy():
                cls._unsubscribe(subscriber, topic)

    ### DECORATORS ###

    @classmethod
    def subscribe_before(cls, topic):
        def decorator(function):
            @functools.wraps(function)
            def wrapper(self, *args, **kwargs):
                cls.subscribe(self, topic)
                return function(self, *args, **kwargs)

            return wrapper

        return decorator

    @classmethod
    def unsubscribe_after(cls, topic):
        def decorator(function):
            @functools.wraps(function)
            def wrapper(self, *args, **kwargs):
                return_value = function(self, *args, **kwargs)
                cls.unsubscribe(self, topic)
                return return_value

            return wrapper

        return decorator
