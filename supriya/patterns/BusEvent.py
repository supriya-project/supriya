import uuid
import supriya.realtime
import supriya.synthdefs
from supriya.patterns.Event import Event


class BusEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate='AUDIO',
        channel_count=1,
        delta=0.0,
        is_stop=False,
        uuid=None,
        **settings,
    ):
        if channel_count is not None:
            assert 0 < channel_count
        if calculation_rate is not None:
            calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        is_stop = bool(is_stop)
        if is_stop:
            calculation_rate = None
            channel_count = None
        settings = {
            key: value for key, value in settings.items() if key.startswith('_')
        }
        Event.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            delta=delta,
            is_stop=is_stop,
            uuid=uuid,
            **settings,
        )

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        bus_uuid = self.get('uuid') or uuid.uuid4()
        if not self.get('is_stop'):
            bus_group = session.add_bus_group(
                bus_count=self['channel_count'],
                calculation_rate=self['calculation_rate'],
            )
            uuids[bus_uuid] = bus_group
        else:
            pass
        return offset + self.delta

    def _perform_realtime(self, index=0, server=None, timestamp=0, uuids=None):
        import supriya.patterns

        bus_uuid = self.get('uuid') or uuid.uuid4()
        calculation_rate = self.get('calculation_rate')
        channel_count = self.get('channel_count') or 1
        if not self.get('is_stop'):
            bus_group = supriya.realtime.BusGroup(
                bus_count=channel_count, calculation_rate=calculation_rate
            )
            allocator = supriya.realtime.Bus._get_allocator(
                calculation_rate=calculation_rate, server=server
            )
            bus_id = allocator.allocate(channel_count)
            uuids[bus_uuid] = {bus_id: bus_group}
        else:
            pass
        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=self.get('is_stop'),
            requests=[],
            timestamp=timestamp,
            uuid=self['uuid'],
        )
        return [event_product]
