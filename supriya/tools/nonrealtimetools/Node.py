# -*- encoding: utf-8 -*-
import bisect
import collections
from abjad import new
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

    def __init__(
        self,
        session,
        session_id,
        duration=None,
        start_offset=None,
        ):
        SessionObject.__init__(self, session)
        self._session_id = int(session_id)
        start_offset = start_offset or 0
        self._start_offset = float(start_offset)
        if duration is None:
            duration = float('inf')
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

    def _add_node(self, node, add_action):
        state = self.session._find_state_at(
            node.start_offset,
            clone_if_missing=True,
            )
        state.start_nodes.add(node)
        if node not in state.nodes_to_children:
            state.nodes_to_children[node] = None
        state = self.session._find_state_at(
            node.stop_offset,
            clone_if_missing=True,
            )
        state.stop_nodes.add(node)
        self.move_node(node, add_action=add_action)
        self.session.nodes.insert(node)
        self.session._apply_transitions([node.start_offset, node.stop_offset])

    def _collect_settings(self, offset, id_mapping=None, persistent=False):
        settings = {}
        if persistent:
            for key in self._events:
                value = self._get_at_offset(offset, key)
                if id_mapping and value in id_mapping:
                    value = id_mapping[value]
                settings[key] = value
        else:
            for key, events in self._events.items():
                events = events[:]
                for i, (event_offset, value) in enumerate(events):
                    # TODO: This is dreadfully inefficient.
                    if id_mapping and value in id_mapping:
                        value = id_mapping[value]
                        events[i] = (event_offset, value)
                index = bisect.bisect_left(events, (offset, 0.))
                if len(events) <= index:
                    continue
                event_offset, value = events[index]
                if offset == event_offset:
                    settings[key] = value
        return settings

    def _fixup_duration(self, new_duration):
        with self.session.at(self.stop_offset, propagate=False) as moment:
            if self in moment.state.stop_nodes:
                moment.state.stop_nodes.remove(self)
        self._duration = new_duration
        with self.session.at(self.stop_offset, propagate=False) as moment:
            moment.state.stop_nodes.add(self)

    def _fixup_events(self, new_node, split_offset):
        left_events, right_events = {}, {}
        for name, events in self._events.items():
            for offset, value in events:
                if offset < split_offset:
                    left_events.setdefault(name, []).append((offset, value))
                else:
                    right_events.setdefault(name, []).append((offset, value))
        for name, events in left_events.items():
            if (name in right_events and
                right_events[name][0][0] == split_offset):
                continue
            event = (split_offset, events[-1][-1])
            right_events.setdefault(name, []).insert(0, event)
        self._events = left_events
        new_node._events = right_events

    def _fixup_node_actions(self, new_node, start_offset, stop_offset):
        for offset in sorted(self.session.states):
            if offset < start_offset:
                continue
            elif stop_offset < offset:
                break
            transitions = self.session.states[offset].transitions
            if self in transitions:
                transitions[new_node] = transitions.pop(self)
            for node, action in transitions.items():
                if node is new_node:
                    continue
                if action.target is self:
                    action._target = new_node

    def _get_at_offset(self, offset, item):
        '''
        Relative to Synth start offset.
        '''
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
        if offset < self.start_offset or self.stop_offset <= offset:
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

    def _split(
        self,
        split_offset,
        new_nodes=None,
        split_occupiers=True,
        split_traversers=True,
        ):
        from supriya.tools import nonrealtimetools
        new_nodes = new_nodes or []
        state = self.session.states[split_offset]
        entering, exiting, occupying, starting, _ = \
            self.inspect_children()
        children = state.nodes_to_children.get(self) or ()
        start_offset, stop_offset = self.start_offset, self.stop_offset
        if start_offset < split_offset < stop_offset:
            old_actions = state.transitions
            new_duration = stop_offset - split_offset
            with nonrealtimetools.DoNotPropagate():
                if isinstance(self, nonrealtimetools.Synth):
                    new_node = self.add_synth(
                        add_action='ADD_BEFORE',
                        duration=new_duration,
                        synthdef=self.synthdef,
                        **self._synth_kwargs
                        )
                else:
                    new_node = self.add_group(
                        add_action='ADD_BEFORE',
                        duration=new_duration,
                        )
            new_nodes.append(new_node)
            new_actions = collections.OrderedDict()
            for node in new_nodes:
                if node is new_node and self in old_actions:
                    old_actions.pop(node)
                    action = old_actions.pop(self)
                    new_actions[node] = new(
                        action,
                        source=new_node,
                        )
                else:
                    new_actions[node] = old_actions.pop(node)
            for child in reversed(children):
                if child in old_actions:
                    old_actions.pop(child)
                action = nonrealtimetools.NodeAction(
                    source=child,
                    target=new_node,
                    action='ADD_TO_TAIL',
                    )
                new_actions[child] = action
            new_actions.update(old_actions)
            state._transitions = new_actions
            self._fixup_events(new_node, split_offset)
            self._fixup_duration(split_offset - start_offset)
            self._fixup_node_actions(new_node, split_offset, stop_offset)
            self.session._apply_transitions(
                [new_node.start_offset, new_node.stop_offset],
                )
            result = [self, new_node]
        else:
            return [self]
        for child in children + exiting:
            if (
                (split_occupiers and child in occupying) or
                (split_traversers and child in entering) or
                (split_traversers and child in exiting)
                ):
                child._split(
                    split_offset,
                    new_nodes=new_nodes,
                    split_occupiers=split_occupiers,
                    split_traversers=split_traversers,
                    )
        return result

    ### CONSTRUCTORS ###

    def add_group(
        self,
        add_action=None,
        duration=None,
        ):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        session_id = self.session._get_next_session_id('node')
        node = nonrealtimetools.Group(
            self.session,
            session_id=session_id,
            duration=duration,
            start_offset=start_moment.offset,
            )
        self._add_node(node, add_action)
        return node

    def add_synth(
        self,
        add_action=None,
        duration=None,
        synthdef=None,
        **synth_kwargs
        ):
        from supriya import synthdefs
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        start_moment = self.session.active_moments[-1]
        session_id = self.session._get_next_session_id('node')
        synthdef = synthdef or synthdefs.default
        node = nonrealtimetools.Synth(
            self.session,
            session_id=session_id,
            duration=duration,
            start_offset=start_moment.offset,
            synthdef=synthdef,
            **synth_kwargs
            )
        self._add_node(node, add_action)
        return node

    ### MUTATORS ###

    def move_node(
        self,
        node,
        add_action=None,
        ):
        from supriya.tools import nonrealtimetools
        assert self.session.active_moments
        state = self.session.active_moments[-1].state
        if state.nodes_to_parents is None:
            state._desparsify()
        if (
            node in state.nodes_to_parents and
            node in self.get_parentage()
            ):
            raise ValueError("Can't add parent as a child.")
        add_action = servertools.AddAction.from_expr(add_action)
        node_action = nonrealtimetools.NodeAction(
            source=node,
            target=self,
            action=add_action,
            )
        state.transitions[node] = node_action
        self.session._apply_transitions([state.offset, node.stop_offset])

    def delete(self):
        #print('DELETING', self)
        start_state = self.session._find_state_at(self.start_offset)
        start_state.start_nodes.remove(self)
        stop_state = self.session._find_state_at(self.stop_offset)
        stop_state.stop_nodes.remove(self)
        start_offset = self.session._find_state_before(
            self.start_offset, with_node_tree=True).offset
        for state_one, state_two in self.session._iterate_state_pairs(
            start_offset, with_node_tree=True):
            state_two._desparsify()
            if self in state_two.nodes_to_children:
                parent = state_two.nodes_to_parents.pop(self)
                inner_children = state_two.nodes_to_children.pop(self) or ()
                outer_children = list(state_two.nodes_to_children[parent])
                index = outer_children.index(self)
                outer_children[index:index + 1] = inner_children
                for child in inner_children:
                    state_two.nodes_to_parents[child] = parent
                children = tuple(outer_children) or None
                state_two.nodes_to_children[parent] = children
            state_two._transitions = state_two._rebuild_transitions(
                state_one, state_two)
            if state_two == self.stop_offset:
                break
        self.session.nodes.remove(self)
        self.session._apply_transitions([self.start_offset, self.stop_offset])

    def set_duration(self, new_duration):
        from supriya.tools import nonrealtimetools
        if self.duration == new_duration:
            return
        if new_duration < self.duration:
            split_offset = self.start_offset + new_duration
            with self.session.at(split_offset):
                old_node, new_node = self.split(
                    split_occupiers=False,
                    split_traversers=False,
                    )
                new_node.delete()
            self.session._find_state_at(new_node.stop_offset)._sparsify()
        else:
            old_stop_offset = self.stop_offset
            new_stop_offset = self.start_offset + new_duration
            with self.session.at(old_stop_offset, propagate=False) as moment:
                parent = self.get_parent()
                moment.state.stop_nodes.remove(self)
                moment.state._sparsify()
            self._duration = new_duration
            while parent is not None and parent.stop_offset < new_stop_offset:
                with self.session.at(parent.stop_offset, propagate=False) as moment:
                    action = nonrealtimetools.NodeAction(
                        source=self,
                        target=parent,
                        action='ADD_BEFORE',
                        )
                    moment.state.transitions[self] = action
                    parent = parent.get_parent()
            with self.session.at(new_stop_offset, propagate=False) as moment:
                moment.state.stop_nodes.add(self)
            with self.session.at(self.start_offset, propagate=False) as moment:
                self.session._apply_transitions(moment.state.offset)
            self.session._apply_transitions([
                self.start_offset,
                old_stop_offset,
                new_stop_offset,
                ])

    def split(
        self,
        split_occupiers=True,
        split_traversers=True,
        ):
        assert self.session.active_moments
        moment = self.session.active_moments[-1]
        state = moment.state
        self.session._apply_transitions(state.offset)
        shards = self._split(
            moment.offset,
            split_occupiers=split_occupiers,
            split_traversers=split_traversers,
            )
        stop_offset = shards[-1].stop_offset
        while state is not None and state.offset <= stop_offset:
            self.session._apply_transitions(state.offset)
            state = self.session._find_state_after(state.offset)
        return shards

    ### RELATIONS ###

    def inspect_children(self, offset=None):
        if offset is None:
            assert self.session.active_moments
            moment = self.session.active_moments[-1]
            this_state = moment.state
            offset = moment.offset
        else:
            this_state = self.session._get_state_at(
                offset,
                clone_if_missing=True,
                )
        prev_state = self.session._find_state_before(this_state.offset, True)
        prev_state._desparsify()
        this_state._desparsify()
        prev_children = prev_state.nodes_to_children.get(self) or ()
        this_children = this_state.nodes_to_children.get(self) or ()
        entering = set()
        exiting = set()
        occupying = set()
        starting = set()
        stopping = set()
        for node in prev_children:
            if node.stop_offset == offset:
                stopping.add(node)
                continue
            if node in this_children:
                occupying.add(node)
            else:
                exiting.add(node)
        for node in this_children:
            if node.start_offset == offset:
                starting.add(node)
                continue
            if node.stop_offset == offset:
                stopping.add(node)
                continue
            if node in prev_children:
                occupying.add(node)
            else:
                entering.add(node)
        entering = tuple(sorted(entering, key=lambda x: x.session_id))
        exiting = tuple(sorted(exiting, key=lambda x: x.session_id))
        occupying = tuple(sorted(occupying, key=lambda x: x.session_id))
        starting = tuple(sorted(starting, key=lambda x: x.session_id))
        stopping = tuple(sorted(stopping, key=lambda x: x.session_id))
        return (entering, exiting, occupying, starting, stopping)

    def get_parent(self):
        assert self.session.active_moments
        state = self.session.active_moments[-1].state
        if not state.nodes_to_children:
            state = self.session._find_state_before(state.offset, True)
        elif self.stop_offset == state.offset:
            state = self.session._find_state_before(state.offset, True)
        return state.nodes_to_parents.get(self) or None

    def get_parentage(self):
        assert self.session.active_moments
        state = self.session.active_moments[-1].state
        if not state.nodes_to_children:
            state = self.session._find_state_before(state.offset, True)
        node = self
        parentage = [node]
        while state.nodes_to_parents[node] is not None:
            parent = state.nodes_to_parents[node]
            parentage.append(parent)
            node = parent
        return parentage

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
