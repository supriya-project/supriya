# -*- encoding: utf-8 -*-
import bisect
from supriya.tools import servertools
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class Node(SessionObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        '_events',
        '_session',
        '_session_id',
        '_start_offset',
        )

    ### INITIALIZER ###

    def __init__(self, session, session_id, duration=None, start_offset=None):
        SessionObject.__init__(self, session)
        if duration is None:
            duration = float('inf')
        self._session_id = int(session_id)
        self._start_offset = float(start_offset)
        self._duration = duration
        self._events = {}

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<{} #{} @{}:{}>'.format(
            type(self).__name__,
            self.session_id,
            self.start_offset,
            self.stop_offset,
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        assert self.session._active_moments
        offset = self.session._active_moments[-1].offset
        return self._get_at_offset(offset, item)

    def __setitem__(self, item, value):
        from supriya.tools import nonrealtimetools
        assert self.session._active_moments
        offset = self.session._active_moments[-1].offset
        assert isinstance(value, (int, float, nonrealtimetools.Bus, nonrealtimetools.BusGroup))
        self._set_at_offset(offset, item, value)

    ### PRIVATE METHODS ###

    def _collect_settings(self, offset):
        settings = {}
        for key, events in self._events.items():
            index = bisect.bisect_left(events, (offset, 0.))
            event_offset, value = events[index]
            if offset == event_offset:
                settings[key] = value
        return settings

    def _get_at_offset(self, offset, item):
        '''
        Relative to Synth start offset.
        '''
        offset -= self.start_offset
        events = self._events.get(item)
        if hasattr(self, 'synthdef'):
            default = self.synthdef.parameters[item].value
            default = self._synth_kwargs.get(item, default)
        else:
            default = None
        if not events:
            return default
        index = bisect.bisect_left(events, (offset, 0.))
        if len(events) <= index:
            old_offset, value = events[-1]
        else:
            old_offset, value = events[index]
        if old_offset == offset:
            return value
        index -= 1
        if index < 0:
            return default
        _, value = events[index]
        return value

    def _set_at_offset(self, offset, item, value):
        '''
        Relative to Synth start offset.
        '''
        offset -= self.start_offset
        if offset < 0 or self.duration < offset:
            return
        events = self._events.setdefault(item, [])
        new_event = (offset, value)
        if not events:
            events.append(new_event)
            return
        index = bisect.bisect_left(events, new_event)
        if len(events) <= index:
            events.append(new_event)
        old_offset, old_value = events[index]
        if old_offset == offset:
            events[index] = (offset, value)
        else:
            events.insert(index, new_event)

    ### PUBLIC METHODS ###

    def add_group(
        self,
        add_action=None,
        ):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        node = nonrealtimetools.Group(
            self.session,
            session_id=len(self.session.nodes) + 1,
            start_offset=start_moment.offset,
            )
        self.move_node(node, add_action=add_action)
        start_moment.start_nodes.add(node)
        self.session.nodes.add(node)
        return node

    def add_synth(
        self,
        add_action=None,
        duration=None,
        synthdef=None,
        **synth_kwargs
        ):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        node = nonrealtimetools.Synth(
            self.session,
            session_id=len(self.session.nodes) + 1,
            duration=duration,
            start_offset=start_moment.offset,
            synthdef=synthdef,
            **synth_kwargs
            )
        self.move_node(node, add_action=add_action)
        start_moment.start_nodes.add(node)
        if node.duration:
            with self.session.at(node.stop_offset) as stop_moment:
                stop_moment.stop_nodes.add(node)
        self.session.nodes.add(node)
        return node

    def move_node(
        self,
        node,
        add_action=None,
        ):
        assert self.session.active_moments
        add_action = servertools.AddAction.from_expr(add_action)
        self.session.active_moments[-1]._register_action(
            source=node,
            target=self,
            action=add_action,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self._duration

    @property
    def session_id(self):
        return self._session_id

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def stop_offset(self):
        if self.duration is None:
            return None
        return self.start_offset + self.duration
