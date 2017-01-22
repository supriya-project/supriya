# -*- encoding: utf-8 -*-
import uuid
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.patterntools.Event import Event


class GroupEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        delta=0.0,
        is_stop=None,
        target_node=None,
        uuid=None,
        **settings
        ):
        if add_action is not None:
            add_action = servertools.AddAction.from_expr(add_action)
        is_stop = is_stop or None
        if is_stop:
            is_stop = bool(is_stop)
            add_action = None
            target_node = None
        settings = {
            key: value for key, value in settings.items()
            if key.startswith('_')
            }
        Event.__init__(
            self,
            add_action=add_action,
            delta=delta,
            is_stop=is_stop,
            target_node=target_node,
            uuid=uuid,
            **settings
            )

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(
        self,
        session,
        uuids,
        offset,
        maximum_offset=None,
        ):
        from supriya.tools import nonrealtimetools
        group_uuid = self.get('uuid', uuid.uuid4())
        if not self.get('is_stop'):
            target_node = self['target_node']
            if isinstance(target_node, uuid.UUID) and target_node in uuids:
                target_node = uuids[target_node]
            prototype = (nonrealtimetools.Session, nonrealtimetools.Node)
            if not isinstance(target_node, prototype):
                target_node = session
            group = target_node.add_group(add_action=self['add_action'])
            uuids[group_uuid] = group
        else:
            group = uuids[group_uuid]
            duration = offset - group.start_offset
            group.set_duration(duration)
        return offset + self.delta

    def _perform_realtime(
        self,
        index=0,
        server=None,
        timestamp=0,
        uuids=None,
        ):
        from supriya.tools import patterntools
        node_uuid = self.get('uuid') or uuid.uuid4()
        requests = []
        if not self.get('is_stop'):
            node_id = server.node_id_allocator.allocate_node_id()
            uuids[node_uuid] = {node_id: servertools.Group()}
            target_node_id = self.get('target_node')
            if not target_node_id:
                target_node_id = 1
            elif isinstance(target_node_id, uuid.UUID):
                target_node_id = list(uuids[target_node_id])[0]
            add_action = self.get('add_action')
            request = requesttools.GroupNewRequest(
                add_action=add_action,
                node_id=node_id,
                target_node_id=target_node_id,
                )
        else:
            request = requesttools.NodeFreeRequest(
                node_ids=sorted(uuids[node_uuid]),
                )
        requests.append(request)
        event_product = patterntools.EventProduct(
            event=self,
            index=index,
            is_stop=self.get('is_stop'),
            requests=requests,
            timestamp=timestamp,
            uuid=self['uuid'],
            )
        return [event_product]
