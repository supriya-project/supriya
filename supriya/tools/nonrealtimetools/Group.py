# -*- encoding: utf-8 -*-
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.Node import Node
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class Group(Node):
    """
    A non-realtime group.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Objects'

    __slots__ = ()

    _valid_add_actions = (
        servertools.AddAction.ADD_TO_HEAD,
        servertools.AddAction.ADD_TO_TAIL,
        servertools.AddAction.ADD_AFTER,
        servertools.AddAction.ADD_BEFORE,
        )

    ### SPECIAL METHODS ###

    def __str__(self):
        return 'group-{}'.format(self.session_id)

    ### PRIVATE METHODS ###

    def _to_request(self, action, id_mapping):
        source_id = id_mapping[action.source]
        target_id = id_mapping[action.target]
        add_action = action.action
        request = requesttools.GroupNewRequest(
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
        from supriya.tools import patterntools

        assert isinstance(pattern, patterntools.Pattern)

        if seed is not None:
            pattern = patterntools.Pseed(
                pattern=pattern,
                seed=seed,
                )

        if duration is None:
            duration = self.stop_offset - offset
        if pattern.is_infinite:
            duration = float(duration)
            assert duration

        should_stop = patterntools.Pattern.PatternState.CONTINUE
        maximum_offset = offset + duration
        actual_stop_offset = offset
        iterator = iter(pattern)
        uuids = {}

        try:
            event = next(iterator)
        except StopIteration:
            return offset

        if (
            duration is not None and
            isinstance(event, patterntools.NoteEvent) and
            self._get_stop_offset(offset, event) > maximum_offset
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
            if (
                maximum_offset is not None and
                isinstance(event, patterntools.NoteEvent) and
                self._get_stop_offset(offset, event) > maximum_offset
                ):
                should_stop = patterntools.Pattern.PatternState.NONREALTIME_STOP
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

        return actual_stop_offset
