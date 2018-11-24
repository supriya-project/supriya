from supriya.patterns.Event import Event


class CompositeEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, delta=0, events=None, is_stop=None, **settings):
        events = events or ()
        events = tuple(events)
        is_stop = is_stop or None
        if is_stop:
            is_stop = bool(is_stop)
        Event.__init__(self, delta=delta, events=events, is_stop=is_stop)

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        for event in self.get('events'):
            event._perform_nonrealtime(
                session=session,
                uuids=uuids,
                offset=offset,
                maximum_offset=maximum_offset,
            )
            offset += event.delta
        return offset

    def _perform_realtime(self, index=None, server=None, timestamp=0, uuids=None):
        event_products = []
        for subindex, event in enumerate(self.get('events')):
            event_products.extend(
                event._perform_realtime(
                    index=(index[0], subindex),
                    server=server,
                    timestamp=timestamp,
                    uuids=uuids,
                )
            )
            timestamp += event.delta
        return event_products
