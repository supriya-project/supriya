import supriya.commands
import supriya.realtime
from supriya.nonrealtime.Node import Node
from supriya.nonrealtime.SessionObject import SessionObject


class Group(Node):
    """
    A non-realtime group.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Objects'

    __slots__ = ()

    _valid_add_actions = (
        supriya.realtime.AddAction.ADD_TO_HEAD,
        supriya.realtime.AddAction.ADD_TO_TAIL,
        supriya.realtime.AddAction.ADD_AFTER,
        supriya.realtime.AddAction.ADD_BEFORE,
        )

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'group-{}'.format(self.session_id)

    ### PRIVATE METHODS ###

    def _to_request(self, action, id_mapping):
        source_id = id_mapping[action.source]
        target_id = id_mapping[action.target]
        add_action = action.action
        request = supriya.commands.GroupNewRequest(
            add_action=add_action,
            node_id=source_id,
            target_node_id=target_id,
            )
        return request

    def _get_stop_offset(self, offset, event):
        duration = event.get('duration') or 0
        delta = event.get('delta') or 0
        return offset + max(duration, delta)

    ### PUBLIC METHODS ###

    @SessionObject.require_offset
    def inscribe(
        self,
        pattern,
        duration=None,
        offset=None,
        seed=None,
        ):
        import supriya.patterns

        assert isinstance(pattern, supriya.patterns.Pattern)

        if seed is not None:
            pattern = supriya.patterns.Pseed(
                pattern=pattern,
                seed=seed,
                )

        if duration is None:
            duration = self.stop_offset - offset
        if pattern.is_infinite:
            duration = float(duration)
            assert duration

        should_stop = supriya.patterns.Pattern.PatternState.CONTINUE
        maximum_offset = offset + duration
        actual_stop_offset = offset
        iterator = iter(pattern)
        uuids = {}

        #print('[INSCRIBE]', 'START')
        try:
            event = next(iterator)
            #print('[INSCRIBE]', type(event).__name__, event.get('frequency') or '')
        except StopIteration:
            #print('[INSCRIBE]', 'DONE')
            return offset

        if (
            duration is not None and
            isinstance(event, supriya.patterns.NoteEvent) and
            self._get_stop_offset(offset, event) > maximum_offset
            ):
            return offset
        performed_stop_offset = event._perform_nonrealtime(
            session=self.session,
            uuids=uuids,
            maximum_offset=maximum_offset,
            offset=offset,
            )
        #print('[INSCRIBE]    START:', offset)
        offset += event.delta
        actual_stop_offset = max(actual_stop_offset, performed_stop_offset)
        #print('[INSCRIBE]    STOP:', actual_stop_offset)
        #print('[INSCRIBE]    NEXT START:', offset)

        while True:
            try:
                event = iterator.send(should_stop)
                #print(
                #    '[INSCRIBE]',
                #    type(event).__name__,
                #    'DELTA', event.delta,
                #    'DUR', event.get('duration'),
                #    'FREQ', event.get('frequency'),
                #    )
            except StopIteration:
                #print('[INSCRIBE]', 'DONE')
                break
            #print('[INSCRIBE]    START:', offset)
            if (
                maximum_offset is not None and
                isinstance(event, supriya.patterns.NoteEvent)
                ):
                if (
                    event.get('duration', 0) == 0 and
                    offset == maximum_offset
                    ):
                    # Current event is 0-duration and we're at our stop.
                    should_stop = supriya.patterns.Pattern.PatternState.NONREALTIME_STOP
                    offset = actual_stop_offset
                    #print('[INSCRIBE]', 'STOPPING EXACT')
                    #print('[INSCRIBE]    STOP:', actual_stop_offset)
                    #print('[INSCRIBE]    NEXT START:', offset)
                    continue
                elif self._get_stop_offset(offset, event) > maximum_offset:
                    # We would legitimately overshoot.
                    should_stop = supriya.patterns.Pattern.PatternState.NONREALTIME_STOP
                    offset = actual_stop_offset
                    #print('[INSCRIBE]', 'STOPPING OVERHANG')
                    #print('[INSCRIBE]    STOP:', actual_stop_offset)
                    #print('[INSCRIBE]    NEXT START:', offset)
                    continue
            performed_stop_offset = event._perform_nonrealtime(
                session=self.session,
                uuids=uuids,
                maximum_offset=maximum_offset,
                offset=offset,
                )
            offset += event.delta
            actual_stop_offset = max(
                actual_stop_offset,
                performed_stop_offset,
                )
            #print('[INSCRIBE]    STOP:', actual_stop_offset)
            #print('[INSCRIBE]    NEXT START:', offset)

        return actual_stop_offset
