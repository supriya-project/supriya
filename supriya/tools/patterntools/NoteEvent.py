import uuid
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.patterntools.Event import Event


class NoteEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        delta=None,
        duration=None,
        is_stop=True,
        synthdef=None,
        target_node=None,
        uuid=None,
        **settings
        ):
        if add_action is not None:
            add_action = servertools.AddAction.from_expr(add_action)
        Event.__init__(
            self,
            add_action=add_action,
            delta=delta,
            duration=duration,
            is_stop=bool(is_stop),
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
        from supriya import synthdefs
        from supriya.tools import nonrealtimetools
        settings = self.settings.copy()  # Do not mutate in place.
        synthdef = self.get('synthdef', synthdefs.default)
        synthdef = synthdef or synthdefs.default
        synth_uuid = self.get('uuid', uuid.uuid4())
        is_stop = self.get('is_stop')
        duration = self.get('duration')
        if duration is None:
            duration = 1
        if 'duration' in settings:
            duration = settings.pop('duration')
        dictionaries = self._expand(
            settings,
            synthdef,
            uuids,
            realtime=False,
            synth_parameters_only=True,
            )
        if synth_uuid not in uuids:
            # Begin a Pbind or Pmono synth
            target_node = self['target_node']
            if isinstance(target_node, uuid.UUID) and target_node in uuids:
                target_node = uuids[target_node]
            prototype = (nonrealtimetools.Session, nonrealtimetools.Node)
            if not isinstance(target_node, prototype):
                target_node = session
            synths = []
            with session.at(offset):
                for dictionary in dictionaries:
                    synth = target_node.add_synth(
                        add_action=self['add_action'],
                        duration=duration,
                        synthdef=synthdef,
                        **dictionary
                        )
                    synths.append(synth)
            if not is_stop:
                uuids[synth_uuid] = tuple(synths)
        else:
            # Extend and make settings on a Pmono synth
            synths = uuids[synth_uuid]
            stop_offset = offset + duration
            for synth, dictionary in zip(synths, dictionaries):
                duration = stop_offset - synth.start_offset
                synth.set_duration(duration)
                with session.at(offset):
                    for key, value in dictionary.items():
                        synth[key] = value
        return offset + max(self.delta, self.get('duration', 0))

    def _perform_realtime(
        self,
        index=0,
        server=None,
        timestamp=0,
        uuids=None,
        ):
        from supriya import synthdefs
        from supriya.tools import patterntools
        synth_uuid = self.get('uuid') or uuid.uuid4()
        synthdef = self.get('synthdef', synthdefs.default)
        synthdef = synthdef or synthdefs.default
        is_stop = self.get('is_stop')
        duration = self['duration']
        if duration is None:
            duration = 1
        dictionaries = self._expand(self.settings, synthdef, uuids)
        first_visit = False
        if synth_uuid not in uuids:
            first_visit = True
            node_ids = {
                server.node_id_allocator.allocate_node_id(): None
                for _ in range(len(dictionaries))
                }
            uuids[synth_uuid] = node_ids
        start_product = self._build_start_bundle(
            dictionaries,
            first_visit,
            index,
            synth_uuid,
            synthdef,
            timestamp,
            uuids,
            )
        if self.get('duration'):
            if is_stop:
                stop_product = self._build_stop_bundle(
                    index,
                    synth_uuid,
                    synthdef,
                    timestamp,
                    uuids,
                    )
            else:
                stop_product = patterntools.EventProduct(
                    event=None,
                    index=index,
                    is_stop=True,
                    requests=(),
                    timestamp=timestamp + duration,
                    uuid=None,
                    )
            return [start_product, stop_product]
        else:
            uuids.pop(synth_uuid)
            return [start_product]

    def _build_start_bundle(
        self,
        dictionaries,
        first_visit,
        index,
        synth_uuid,
        synthdef,
        timestamp,
        uuids,
        ):
        from supriya.tools import patterntools
        requests = []
        node_ids = uuids[synth_uuid]
        if first_visit:
            for node_id, dictionary in zip(node_ids, dictionaries):
                add_action = dictionary.pop('add_action')
                target_node = dictionary.pop('target_node')
                if target_node is None:
                    target_node = 1
                synth_kwargs = {
                    key: value for key, value in dictionary.items()
                    if key in synthdef.parameter_names
                    }
                request = requesttools.SynthNewRequest(
                    add_action=add_action,
                    node_id=node_id,
                    synthdef=synthdef,
                    target_node_id=target_node,
                    **synth_kwargs
                    )
                requests.append(request)
                synth = servertools.Synth(synthdef)
                node_ids[node_id] = synth
        else:
            for node_id, dictionary in zip(node_ids, dictionaries):
                synth_kwargs = {
                    key: value for key, value in dictionary.items()
                    if key in synthdef.parameter_names
                    }
                request = requesttools.NodeSetRequest(
                    node_id=node_id,
                    **synth_kwargs
                    )
                requests.append(request)
        event_product = patterntools.EventProduct(
            event=self,
            index=index,
            is_stop=False,
            requests=requests,
            timestamp=timestamp,
            uuid=synth_uuid,
            )
        return event_product

    def _build_stop_bundle(
        self,
        index,
        synth_uuid,
        synthdef,
        timestamp,
        uuids,
        ):
        from supriya.tools import patterntools
        from supriya.tools import synthdeftools
        duration = self['duration']
        if duration is None:
            duration = 1
        requests = []
        timestamp = timestamp + duration
        node_ids = sorted(uuids[synth_uuid])
        if synthdef.has_gate:
            for node_id in node_ids:
                request = requesttools.NodeSetRequest(
                    node_id=node_id,
                    gate=0,
                    )
                requests.append(request)
        elif any(
            x >= synthdeftools.DoneAction.FREE_SYNTH
            for x in synthdef.done_actions
            ):
            pass
        else:
            request = requesttools.NodeFreeRequest(
                node_ids=node_ids,
                )
            requests.append(request)
        event_product = patterntools.EventProduct(
            event=self,
            index=index,
            is_stop=True,
            requests=requests,
            timestamp=timestamp,
            uuid=synth_uuid,
            )
        return event_product
