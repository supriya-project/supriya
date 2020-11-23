import uuid

import supriya.commands
import supriya.realtime
import supriya.synthdefs

from .bases import Event


class BusEvent(Event):

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate="AUDIO",
        channel_count=1,
        delta=0.0,
        is_stop=False,
        uuid=None,
        **settings,
    ):
        if channel_count is not None:
            assert 0 < channel_count
        if calculation_rate is not None:
            calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        is_stop = bool(is_stop)
        if is_stop:
            calculation_rate = None
            channel_count = None
        settings = {
            key: value for key, value in settings.items() if key.startswith("_")
        }
        Event.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            delta=delta,
            is_stop=is_stop,
            uuid=uuid,
            **settings,
        )

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        bus_uuid = self.get("uuid") or uuid.uuid4()
        if not self.get("is_stop"):
            bus_group = session.add_bus_group(
                bus_count=self["channel_count"],
                calculation_rate=self["calculation_rate"],
            )
            uuids[bus_uuid] = bus_group
        else:
            pass
        return offset + self.delta

    def _perform_realtime(self, index=0, server=None, timestamp=0, uuids=None):
        import supriya.patterns

        bus_uuid = self.get("uuid") or uuid.uuid4()
        calculation_rate = self.get("calculation_rate")
        channel_count = self.get("channel_count") or 1
        if not self.get("is_stop"):
            bus_group = supriya.realtime.BusGroup(
                bus_count=channel_count, calculation_rate=calculation_rate
            )
            allocator = supriya.realtime.Bus._get_allocator(
                calculation_rate=calculation_rate, server=server
            )
            bus_id = allocator.allocate(channel_count)
            uuids[bus_uuid] = {bus_id: bus_group}
        else:
            pass
        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=self.get("is_stop"),
            requests=[],
            timestamp=timestamp,
            uuid=self["uuid"],
        )
        return [event_product]


class CompositeEvent(Event):

    ### INITIALIZER ###

    def __init__(self, delta=0, events=None, is_stop=None, **settings):
        events = events or ()
        events = tuple(events)
        is_stop = is_stop or None
        if is_stop:
            is_stop = bool(is_stop)
        Event.__init__(self, delta=delta, events=events, is_stop=is_stop)

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        for event in self.get("events"):
            event._perform_nonrealtime(
                session=session,
                uuids=uuids,
                offset=offset,
                maximum_offset=maximum_offset,
            )
            offset += event.delta
        return offset

    def _perform_realtime(self, index=None, server=None, timestamp=0, uuids=None):
        event_products = []
        for subindex, event in enumerate(self.get("events")):
            event_products.extend(
                event._perform_realtime(
                    index=(index[0], subindex),
                    server=server,
                    timestamp=timestamp,
                    uuids=uuids,
                )
            )
            timestamp += event.delta
        return event_products


class GroupEvent(Event):

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        delta=0.0,
        is_stop=False,
        target_node=None,
        uuid=None,
        **settings,
    ):
        if add_action is not None:
            add_action = supriya.AddAction.from_expr(add_action)
        is_stop = bool(is_stop)
        if is_stop:
            add_action = None
            target_node = None
        settings = {
            key: value for key, value in settings.items() if key.startswith("_")
        }
        Event.__init__(
            self,
            add_action=add_action,
            delta=delta,
            is_stop=is_stop,
            target_node=target_node,
            uuid=uuid,
            **settings,
        )

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        import supriya.nonrealtime

        group_uuid = self.get("uuid", uuid.uuid4())
        if not self.get("is_stop"):
            target_node = self["target_node"]
            if isinstance(target_node, uuid.UUID) and target_node in uuids:
                target_node = uuids[target_node]
            prototype = (supriya.nonrealtime.Session, supriya.nonrealtime.Node)
            if not isinstance(target_node, prototype):
                target_node = session
            group = target_node.add_group(add_action=self["add_action"])
            uuids[group_uuid] = group
        else:
            group = uuids[group_uuid]
            duration = offset - group.start_offset
            group.set_duration(duration, clip_children=True)
        return offset + self.delta

    def _perform_realtime(self, index=0, server=None, timestamp=0, uuids=None):
        import supriya.patterns

        node_uuid = self.get("uuid") or uuid.uuid4()
        requests = []
        if not self.get("is_stop"):
            node_id = server.node_id_allocator.allocate_node_id()
            uuids[node_uuid] = {node_id: supriya.realtime.Group()}
            target_node_id = self.get("target_node")
            if not target_node_id:
                target_node_id = 1
            elif isinstance(target_node_id, uuid.UUID):
                target_node_id = list(uuids[target_node_id])[0]
            add_action = self.get("add_action")
            request = supriya.commands.GroupNewRequest(
                items=[
                    supriya.commands.GroupNewRequest.Item(
                        add_action=add_action,
                        node_id=node_id,
                        target_node_id=target_node_id,
                    )
                ]
            )
        else:
            request = supriya.commands.NodeFreeRequest(
                node_ids=sorted(uuids[node_uuid])
            )
        requests.append(request)
        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=self.get("is_stop"),
            requests=requests,
            timestamp=timestamp,
            uuid=self["uuid"],
        )
        return [event_product]


class NoteEvent(Event):

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
        **settings,
    ):
        if add_action is not None:
            add_action = supriya.AddAction.from_expr(add_action)
        Event.__init__(
            self,
            add_action=add_action,
            delta=delta,
            duration=duration,
            is_stop=bool(is_stop),
            synthdef=synthdef,
            target_node=target_node,
            uuid=uuid,
            **settings,
        )

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        import supriya.assets.synthdefs

        settings = self.settings.copy()  # Do not mutate in place.
        synthdef = self.get("synthdef", supriya.assets.synthdefs.default)
        synthdef = synthdef or supriya.assets.synthdefs.default
        synth_uuid = self.get("uuid", uuid.uuid4())
        is_stop = self.get("is_stop")
        duration = self.get("duration")
        if duration is None:
            duration = 1
        if "duration" in settings:
            duration = settings.pop("duration")
        dictionaries = self._expand(
            settings, synthdef, uuids, realtime=False, synth_parameters_only=True
        )
        if synth_uuid not in uuids:
            # Begin a Pbind or Pmono synth
            target_node = self["target_node"]
            if isinstance(target_node, uuid.UUID) and target_node in uuids:
                target_node = uuids[target_node]
            prototype = (supriya.nonrealtime.Session, supriya.nonrealtime.Node)
            if not isinstance(target_node, prototype):
                target_node = session
            synths = []
            with session.at(offset):
                for dictionary in dictionaries:
                    synth = target_node.add_synth(
                        add_action=self["add_action"],
                        duration=duration,
                        synthdef=synthdef,
                        **dictionary,
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
        return offset + max(self.delta, self.get("duration", 0))

    def _perform_realtime(self, index=0, server=None, timestamp=0, uuids=None):
        import supriya.assets.synthdefs
        import supriya.patterns

        synth_uuid = self.get("uuid") or uuid.uuid4()
        synthdef = self.get("synthdef", supriya.assets.synthdefs.default)
        synthdef = synthdef or supriya.assets.synthdefs.default
        is_stop = self.get("is_stop")
        duration = self["duration"]
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
            dictionaries, first_visit, index, synth_uuid, synthdef, timestamp, uuids
        )
        if self.get("duration"):
            if is_stop:
                stop_product = self._build_stop_bundle(
                    index, synth_uuid, synthdef, timestamp, uuids
                )
            else:
                stop_product = supriya.patterns.EventProduct(
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
        self, dictionaries, first_visit, index, synth_uuid, synthdef, timestamp, uuids
    ):
        import supriya.patterns

        requests = []
        node_ids = uuids[synth_uuid]
        if first_visit:
            for node_id, dictionary in zip(node_ids, dictionaries):
                add_action = dictionary.pop("add_action")
                target_node = dictionary.pop("target_node")
                if target_node is None:
                    target_node = 1
                synth_kwargs = {
                    key: value
                    for key, value in dictionary.items()
                    if key in synthdef.parameter_names
                }
                request = supriya.commands.SynthNewRequest(
                    add_action=add_action,
                    node_id=node_id,
                    synthdef=synthdef,
                    target_node_id=target_node,
                    **synth_kwargs,
                )
                requests.append(request)
                synth = supriya.realtime.Synth(synthdef)
                node_ids[node_id] = synth
        else:
            for node_id, dictionary in zip(node_ids, dictionaries):
                synth_kwargs = {
                    key: value
                    for key, value in dictionary.items()
                    if key in synthdef.parameter_names
                }
                request = supriya.commands.NodeSetRequest(
                    node_id=node_id, **synth_kwargs
                )
                requests.append(request)
        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=False,
            requests=requests,
            timestamp=timestamp,
            uuid=synth_uuid,
        )
        return event_product

    def _build_stop_bundle(self, index, synth_uuid, synthdef, timestamp, uuids):
        import supriya.patterns
        import supriya.synthdefs

        duration = self["duration"]
        if duration is None:
            duration = 1
        requests = []
        timestamp = timestamp + duration
        node_ids = sorted(uuids[synth_uuid])
        if synthdef.has_gate:
            for node_id in node_ids:
                request = supriya.commands.NodeSetRequest(node_id=node_id, gate=0)
                requests.append(request)
        elif any(x >= supriya.DoneAction.FREE_SYNTH for x in synthdef.done_actions):
            pass
        else:
            request = supriya.commands.NodeFreeRequest(node_ids=node_ids)
            requests.append(request)
        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=True,
            requests=requests,
            timestamp=timestamp,
            uuid=synth_uuid,
        )
        return event_product


class NullEvent(Event):

    ### INITIALIZER ###

    def __init__(self, delta=0, uuid=None, **settings):
        settings = {
            key: value for key, value in settings.items() if key.startswith("_")
        }
        Event.__init__(self, delta=delta, uuid=None, **settings)

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        return offset + self.delta

    def _perform_realtime(self, index=0, server=None, timestamp=0, uuids=None):
        import supriya.patterns

        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=False,
            requests=[],
            timestamp=timestamp,
            uuid=self["uuid"],
        )
        event_products = [event_product]
        return event_products


class SynthEvent(Event):

    ### INITIALIZER ###

    def __init__(
        self,
        add_action=None,
        delta=0.0,
        is_stop=False,
        synthdef=None,
        target_node=None,
        uuid=None,
        **settings,
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
            **settings,
        )

    ### PRIVATE METHODS ###

    def _perform_nonrealtime(self, session, uuids, offset, maximum_offset=None):
        import supriya.assets.synthdefs
        import supriya.nonrealtime

        synthdef = self.get("synthdef") or supriya.assets.synthdefs.default
        synth_uuid = self.get("uuid", uuid.uuid4())
        if not self.get("is_stop"):
            target_node = self["target_node"]
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
                        add_action=self["add_action"],
                        duration=float("inf"),
                        synthdef=synthdef,
                        **dictionary,
                    )
                    synths.append(synth)
            uuids[synth_uuid] = tuple(synths)
        else:
            synths = uuids[synth_uuid]
            for synth in synths:
                duration = offset - synth.start_offset
                synth.set_duration(duration)
        return offset + self.delta

    def _perform_realtime(self, index=0, server=None, timestamp=0, uuids=None):
        # TODO: Should this handle multichannel expansion?
        import supriya.assets.synthdefs
        import supriya.patterns

        node_uuid = self.get("uuid") or uuid.uuid4()
        requests = []
        synthdef = self.get("synthdef") or supriya.assets.synthdefs.default
        if not self.get("is_stop"):
            target_node_id = self.get("target_node")
            if not target_node_id:
                target_node_id = 1
            elif isinstance(target_node_id, uuid.UUID):
                target_node_id = list(uuids[target_node_id])[0]
            add_action = self.get("add_action")
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
                    **dictionary,
                )
            requests.append(request)
        else:
            request = supriya.commands.NodeFreeRequest(
                node_ids=sorted(uuids[node_uuid])
            )
            requests.append(request)
        event_product = supriya.patterns.EventProduct(
            event=self,
            index=index,
            is_stop=self.get("is_stop"),
            requests=requests,
            timestamp=timestamp,
            uuid=self["uuid"],
        )
        return [event_product]
