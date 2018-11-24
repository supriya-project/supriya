from supriya.patterns.Event import Event


class NullEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, delta=0, uuid=None, **settings):
        settings = {
            key: value for key, value in settings.items() if key.startswith('_')
        }
        Event.__init__(self, delta=delta, uuid=None, **settings)

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        return offset + self.delta

    def _perform_realtime(self, index=0, server=None, timestamp=0, uuids=None):
        import supriya.patterns

        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=False,
            requests=[],
            timestamp=timestamp,
            uuid=self['uuid'],
        )
        event_products = [event_product]
        return event_products
