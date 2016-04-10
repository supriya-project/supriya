# -*- encoding: utf-8 -*-
import uuid
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.patterntools.Event import Event


class SynthEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        delta=0,
        is_stop=None,
        synthdef=None,
        target_node=None,
        uuid=None,
        **settings
        ):
        if add_action is not None:
            add_action = servertools.AddAction.from_expr(add_action)
        is_stop = is_stop or None
        if is_stop:
            is_stop = bool(is_stop)
        Event.__init__(
            self,
            add_action=add_action,
            delta=delta,
            is_stop=is_stop,
            synthdef=synthdef,
            target_node=target_node,
            uuid=uuid,
            **settings
            )

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self):
        raise NotImplementedError

    def _perform_realtime(
        self,
        index=0,
        server=None,
        timestamp=0,
        uuids=None,
        ):
        from supriya import synthdefs
        from supriya.tools import patterntools
        node_uuid = self.get('uuid') or uuid.uuid4()
        requests = []
        synthdef = self.get('synthdef') or synthdefs.default
        if not self.get('is_stop'):
            node_id = server.node_id_allocator.allocate_node_id()
            uuids[node_uuid] = {
                node_id: servertools.Synth(synthdef),
                }
            target_node_id = self.get('target_node')
            if not target_node_id:
                target_node_id = 1
            elif isinstance(target_node_id, uuid.UUID):
                target_node_id = list(uuids[target_node_id])[0]
            add_action = self.get('add_action')
            settings = self.settings.copy()
            parameter_names = synthdef.parameter_names
            for key in tuple(settings.keys()):
                if key not in parameter_names:
                    settings.pop(key)
            request = requesttools.SynthNewRequest(
                add_action=add_action,
                node_id=node_id,
                target_node_id=target_node_id,
                synthdef=synthdef,
                **settings
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
