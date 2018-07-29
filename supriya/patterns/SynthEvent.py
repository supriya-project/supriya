import uuid
import supriya.commands
import supriya.realtime
from supriya.patterns.Event import Event


class SynthEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        delta=0.0,
        is_stop=False,
        synthdef=None,
        target_node=None,
        uuid=None,
        **settings
        ):
        if add_action is not None:
            add_action = supriya.AddAction.from_expr(add_action)
        is_stop = bool(is_stop)
        if is_stop:
            add_action = None
            synthdef = None
            target_node = None
            settings = {}
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

    def _perform_nonrealtime(
        self,
        session,
        uuids,
        offset,
        maximum_offset=None,
        ):
        import supriya.assets.synthdefs
        import supriya.nonrealtime
        synthdef = self.get('synthdef') or supriya.assets.synthdefs.default
        synth_uuid = self.get('uuid', uuid.uuid4())
        if not self.get('is_stop'):
            target_node = self['target_node']
            if isinstance(target_node, uuid.UUID) and target_node in uuids:
                target_node = uuids[target_node]
            prototype = (supriya.nonrealtime.Session, supriya.nonrealtime.Node)
            if not isinstance(target_node, prototype):
                target_node = session
            dictionaries = self._expand(
                self.settings,
                synthdef,
                uuids,
                realtime=False,
                synth_parameters_only=True,
                )
            synths = []
            with session.at(offset):
                for dictionary in dictionaries:
                    synth = target_node.add_synth(
                        add_action=self['add_action'],
                        duration=float('inf'),
                        synthdef=synthdef,
                        **dictionary
                        )
                    synths.append(synth)
            uuids[synth_uuid] = tuple(synths)
        else:
            synths = uuids[synth_uuid]
            for synth in synths:
                duration = offset - synth.start_offset
                synth.set_duration(duration)
        return offset + self.delta

    def _perform_realtime(
        self,
        index=0,
        server=None,
        timestamp=0,
        uuids=None,
        ):
        # TODO: Should this handle multichannel expansion?
        import supriya.assets.synthdefs
        import supriya.patterns
        node_uuid = self.get('uuid') or uuid.uuid4()
        requests = []
        synthdef = self.get('synthdef') or supriya.assets.synthdefs.default
        if not self.get('is_stop'):
            target_node_id = self.get('target_node')
            if not target_node_id:
                target_node_id = 1
            elif isinstance(target_node_id, uuid.UUID):
                target_node_id = list(uuids[target_node_id])[0]
            add_action = self.get('add_action')
            dictionaries = self._expand(
                self.settings,
                synthdef,
                uuids,
                realtime=False,
                synth_parameters_only=True,
                )
            synths = uuids[node_uuid] = {}
            for dictionary in dictionaries:
                node_id = server.node_id_allocator.allocate_node_id()
                synth = supriya.realtime.Synth(synthdef, **dictionary)
                synths[node_id] = synth
                request = supriya.commands.SynthNewRequest(
                    add_action=add_action,
                    node_id=node_id,
                    target_node_id=target_node_id,
                    synthdef=synthdef,
                    **dictionary
                    )
            requests.append(request)
        else:
            request = supriya.commands.NodeFreeRequest(
                node_ids=sorted(uuids[node_uuid]),
                )
            requests.append(request)
        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=self.get('is_stop'),
            requests=requests,
            timestamp=timestamp,
            uuid=self['uuid'],
            )
        return [event_product]
