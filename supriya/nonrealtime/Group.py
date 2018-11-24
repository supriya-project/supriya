import uuid
import supriya.realtime
from supriya.commands import GroupNewRequest
from supriya.nonrealtime.Node import Node
from supriya.nonrealtime.SessionObject import SessionObject
from supriya.nonrealtime.NodeAction import NodeAction
from supriya.patterns import Pattern
from typing import Dict, Tuple


class Group(Node):
    """
    A non-realtime group.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Objects'

    __slots__ = ()

    _valid_add_actions: Tuple[int, ...] = (
        supriya.AddAction.ADD_TO_HEAD,
        supriya.AddAction.ADD_TO_TAIL,
        supriya.AddAction.ADD_AFTER,
        supriya.AddAction.ADD_BEFORE,
    )

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'group-{}'.format(self.session_id)

    ### PRIVATE METHODS ###

    def _to_request(
        self, action: NodeAction, id_mapping: Dict[SessionObject, int]
    ) -> GroupNewRequest:
        source_id = id_mapping[action.source]
        target_id = id_mapping[action.target]
        add_action = action.action
        request = GroupNewRequest(
            items=[
                GroupNewRequest.Item(
                    add_action=add_action, node_id=source_id, target_node_id=target_id
                )
            ]
        )
        return request

    def _get_stop_offset(self, offset, event) -> float:
        duration = event.get('duration') or 0
        delta = event.get('delta') or 0
        return offset + max(duration, delta)

    ### PUBLIC METHODS ###

    @SessionObject.require_offset
    def inscribe(
        self,
        pattern: Pattern,
        duration: float = None,
        offset: float = None,
        seed: int = None,
    ) -> float:
        import supriya.patterns

        if offset is None:
            raise ValueError(offset)
        assert isinstance(pattern, supriya.patterns.Pattern)
        if seed is not None:
            pattern = supriya.patterns.Pseed(pattern=pattern, seed=seed)
        if duration is None:
            duration = self.stop_offset - offset
        if pattern.is_infinite:
            if duration is None:
                raise ValueError(duration)
            duration = float(duration)
            assert duration
        if duration is None:
            raise ValueError(duration)
        should_stop = supriya.patterns.Pattern.PatternState.CONTINUE
        maximum_offset = offset + duration
        actual_stop_offset = offset
        iterator = pattern.__iter__()
        uuids: Dict[uuid.UUID, Tuple[Node]] = {}
        try:
            event = next(iterator)
        except StopIteration:
            return offset
        if (
            duration is not None
            and isinstance(event, supriya.patterns.NoteEvent)
            and self._get_stop_offset(offset, event) > maximum_offset
        ):
            return offset
        performed_stop_offset = event._perform_nonrealtime(
            session=self.session,
            uuids=uuids,
            maximum_offset=maximum_offset,
            offset=offset,
        )
        offset += event.delta
        actual_stop_offset = max(actual_stop_offset, performed_stop_offset)
        while True:
            try:
                event = iterator.send(should_stop)
            except StopIteration:
                break
            if maximum_offset is not None and isinstance(
                event, supriya.patterns.NoteEvent
            ):
                if event.get('duration', 0) == 0 and offset == maximum_offset:
                    # Current event is 0-duration and we're at our stop.
                    should_stop = supriya.patterns.Pattern.PatternState.NONREALTIME_STOP
                    offset = actual_stop_offset
                    continue
                elif self._get_stop_offset(offset, event) > maximum_offset:
                    # We would legitimately overshoot.
                    should_stop = supriya.patterns.Pattern.PatternState.NONREALTIME_STOP
                    offset = actual_stop_offset
                    continue
            performed_stop_offset = event._perform_nonrealtime(
                session=self.session,
                uuids=uuids,
                maximum_offset=maximum_offset,
                offset=offset,
            )
            offset += event.delta
            actual_stop_offset = max(actual_stop_offset, performed_stop_offset)
        return actual_stop_offset
