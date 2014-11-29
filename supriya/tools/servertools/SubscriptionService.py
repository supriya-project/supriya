# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SubscriptionService(SupriyaObject):

    ### CLASS VARIABLES ###

    Subscription = collections.namedtuple(
        'Subscription',
        ('subscriber', 'topic'),
        verbose=False,
        )

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_subscriptions',
        )

    ### INITIALIZER ###

    def __init__(self):
        self.clear()

    ### PUBLIC METHODS ###

    def clear(self):
        self._subscriptions = {}

    def notify(self, topic, event):
        subscriptions = self._subscriptions.get(topic, ())
        for subscription in subscriptions:
            subscription.subscriber.notify(topic, event)

    def subscribe(self, subscriber, topic):
        subscription = SubscriptionService.Subscription(
            subscriber=subscriber,
            topic=topic,
            )
        if topic not in self._subscriptions:
            self._subscriptions = set()
        subscriptions = self._subscriptions[topic]
        subscriptions.add(subscription)

    def unsubscribe(self, subscriber, topic):
        if topic not in self.subscriptions:
            return
        subscriptions = self._subscriptions[topic]
        for subscription in subscriptions:
            if subscription.subscriber is subscriber:
                subscriptions.remove(subscription)
        if not subscriptions:
            del(self.subscriptions[topic])

    def unsubscribe_all(self, subscriber):
        for topic, subscriptions in tuple(self.subscriptions.items()):
            for subscription in subscriptions[:]:
                if subscription.subscriber is subscriber:
                    subscriptions.remove(subscription)
            if not subscriptions:
                del(self.subscriptions[topic])