# -*- encoding: utf-8 -*-
import uuid
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools.patterntools.Event import Event


class NoteEvent(Event):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        delta=None,
        duration=1,
        target_node=None,
        uuid=None,
        **settings
        ):
        if add_action is not None:
            add_action = servertools.AddAction.from_expr(add_action)
        self._duration = duration
        Event.__init__(
            self,
            add_action=add_action,
            delta=delta,
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
        ):
        from supriya import synthdefs
        synthdef = self.get('synthdef', synthdefs.default)
        synth_uuid = self.get('uuid', uuid.uuid4())
        do_not_release = self.get('_do_not_release')
        if do_not_release:
            timeline = uuids.setdefault(synth_uuid, {})
            timeline.setdefault(offset, []).append(self)
        elif synth_uuid in uuids:
            # Pmono: release it
            timeline = uuids[synth_uuid]
            timeline.setdefault(offset, []).append(self)
            offsets = sorted(timeline)
            start_offset = offsets[0]
            stop_offset = offset + self.duration
            duration = stop_offset - start_offset
            for offset in offsets:
                events = timeline[offset]
                settings = events[0].settings
                for event in events[1:]:
                    settings.update(event.settings)
                timeline[offset] = self._expand(
                    settings, synthdef, uuids)
            synths = []
            with session.at(offsets[0]):
                for synth_kwargs in timeline[offsets[0]]:
                    synth = session.add_synth(
                        duration=duration,
                        synthdef=synthdef,
                        **synth_kwargs
                        )
                    synths.append(synth)
            for offset in offsets[1:]:
                with session.at(offset):
                    for synth, synth_kwargs in zip(synths, timeline[offset]):
                        for key, value in synth_kwargs.items():
                            synth[key] = value
        else:
            # One shot
            expanded_synth_kwargs = self._expand(
                self.settings, synthdef, uuids)
            with session.at(offset):
                for synth_kwargs in expanded_synth_kwargs:
                    synth = session.add_synth(
                        duration=self.duration,
                        synthdef=synthdef,
                        **synth_kwargs
                        )

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
        do_not_release = self.get('_do_not_release')
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
        if not do_not_release:
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
                timestamp=timestamp + self.duration,
                uuid=None,
                )
        node_ids = uuids[synth_uuid]
        return [start_product, stop_product]

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
                request = requesttools.NodeSetRequest(
                    node_id=node_id,
                    **dictionary
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
        requests = []
        timestamp = timestamp + self.duration
        node_ids = uuids[synth_uuid]
        if synthdef.has_gate:
            for node_id in node_ids:
                request = requesttools.NodeSetRequest(
                    node_id=node_id,
                    gate=0,
                    )
                requests.append(request)
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
