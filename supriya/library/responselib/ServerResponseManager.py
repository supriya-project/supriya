# -*- encoding: utf-8 -*-
import itertools
import sys


class ServerResponseManager(object):
    r'''Handles OSC responses from scsynth.

    ::

        >>> from supriya import osclib
        >>> from supriya import responselib
        >>> manager = responselib.ServerResponseManager()

    ::

        >>> message = osclib.OscMessage(
        ...     '/status.reply', 1, 0, 0, 2, 4,
        ...     0.040679048746824265, 0.15118031203746796,
        ...     44100.0, 44100.00077873274,
        ...     )
        >>> manager(message)
        StatusResponse(
            ugen_count=0,
            synth_count=0,
            group_count=2,
            synth_definition_count=4,
            average_cpu_usage=0.040679048746824265,
            peak_cpu_usage=0.15118031203746796,
            target_sample_rate=44100.0,
            actual_sample_rate=44100.00077873274
            )

    ::

        >>> message = osclib.OscMessage('/b_info', 1100, 512, 1, 44100.0)
        >>> manager(message)
        BufferInfoResponse(
            buffer_id=1100,
            frame_count=512,
            channel_count=1,
            sample_rate=44100.0
            )

    ::

        >>> message = osclib.OscMessage('/n_set', 1023, '/one', -1, '/two', 0)
        >>> manager(message)
        NodeSetResponse(
            node_id=1023,
            items=(
                NodeSetItem(
                    control_index_or_name='/one',
                    control_value=-1
                    ),
                NodeSetItem(
                    control_index_or_name='/two',
                    control_value=0
                    ),
                )
            )

    ::

        >>> message = osclib.OscMessage('/b_setn', 1, 0, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        >>> manager(message)
        BufferSetContiguousResponse(
            items=(
                BufferSetContiguousItem(
                    starting_sample_index=0,
                    sample_values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                    ),
                ),
            buffer_number=1
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_response_handlers'
        )

    ### INITIALIZER ###

    def __init__(self):
        self._response_handlers = {
            '/b_info': self._handle_b_info,
            '/b_set': self._handle_b_set,
            '/b_setn': self._handle_b_setn,
            '/c_set': self._handle_c_set,
            '/c_setn': self._handle_c_setn,
            '/done': self._handle_done,
            '/fail': self._handle_fail,
            '/g_queryTree.reply': self._handle_g_query_tree_reply,
            '/n_end': self._handle_n_info,
            '/n_go': self._handle_n_info,
            '/n_info': self._handle_n_info,
            '/n_move': self._handle_n_info,
            '/n_off': self._handle_n_info,
            '/n_on': self._handle_n_info,
            '/n_set': self._handle_n_set,
            '/n_setn': self._handle_n_setn,
            '/status.reply': self._handle_status_reply,
            '/synced': self._handle_synced,
            '/tr': self._handle_tr,
            }

    ### PRIVATE METHODS ###

    def _group_items(self, items, length):
        iterators = [iter(items)] * length
        if sys.version_info[0] == 2:
            iterator = itertools.izip(*iterators)
        else:
            iterator = zip(*iterators)
        return iterator

    def _handle_b_info(self, command, contents):
        from supriya.library import responselib
        arguments = contents
        response = responselib.BufferInfoResponse(*arguments)
        return response

    def _handle_b_set(self, command, contents):
        from supriya.library import responselib
        buffer_number, remainder = contents[0], contents[1:]
        items = []
        for group in self._group_items(remainder, 2):
            item = responselib.BufferSetItem(*group)
            items.append(item)
        items = tuple(items)
        response = responselib.BufferSetResponse(
            buffer_number=buffer_number,
            items=items,
            )
        return response

    def _handle_b_setn(self, command, contents):
        from supriya.library import responselib
        buffer_number, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            starting_sample_index = remainder[0]
            sample_count = remainder[1]
            sample_values = tuple(remainder[2:2 + sample_count])
            item = responselib.BufferSetContiguousItem(
                starting_sample_index=starting_sample_index,
                sample_values=sample_values,
                )
            items.append(item)
            remainder = remainder[2 + sample_count:]
        items = tuple(items)
        response = responselib.BufferSetContiguousResponse(
            buffer_number=buffer_number,
            items=items,
            )
        return response

    def _handle_c_set(self, command, contents):
        from supriya.library import responselib
        items = []
        for group in self._group_items(contents, 2):
            item = responselib.ControlBusSetItem(*group)
            items.append(item)
        response = responselib.ControlBusSetResponse(
            items=tuple(items),
            )
        return response

    def _handle_c_setn(self, command, contents):
        from supriya.library import responselib
        items = []
        while contents:
            starting_bus_index = contents[0]
            bus_count = contents[1]
            bus_values = tuple(contents[2:2 + bus_count])
            item = responselib.ControlBusSetContiguousItem(
                starting_bus_index=starting_bus_index,
                bus_values=bus_values,
                )
            items.append(item)
            contents = contents[2 + bus_count:]
        items = tuple(items)
        response = responselib.CSetnResponse(
            items=items,
            )
        return response

    def _handle_done(self, command, contents):
        from supriya.library import responselib
        arguments = contents
        response = responselib.DoneResponse(*arguments)
        return response

    def _handle_fail(self, command, contents):
        from supriya.library import responselib
        arguments = contents
        response = responselib.FailResponse(*arguments)
        return response

    def _handle_g_query_tree_reply(self, command, contents):
        from supriya.library import responselib
        control_flag = contents[0]
        node_id = contents[1]
        child_count = contents[2]
        contents = contents[3:]
        items = []
        while contents:
            child_node_id = contents[0]
            child_child_count = contents[1]
            contents = contents[2:]
            if 0 <= child_count:
                item = responselib.QueryTreeGroupItem(
                    node_id=child_node_id,
                    child_count=child_child_count,
                    )
            else:
                synth_definition_name = contents[0]
                contents = contents[1:]
                control_items = []
                if control_flag:
                    control_count = contents[0]
                    contents = contents[1:]
                    for _ in control_count:
                        control_name_or_index = contents[0]
                        control_value = contents[1]
                        contents = contents[2:]
                        control_item = responselib.QueryTreeSynthControlItem(
                            control_name_or_index=control_name_or_index,
                            control_value=control_value,
                            )
                        control_items.append(control_item)
                control_items = tuple(control_items)
                item = responselib.QueryTreeSynthItem(
                    node_id=child_node_id,
                    synth_definition_name=synth_definition_name,
                    control_items=control_items,
                    )
            items.append(item)
        items = tuple(items)
        response = responselib.QueryTreeResponse(
            node_id=node_id,
            child_count=child_count,
            items=items,
            )
        return response

    def _handle_n_info(self, command, contents):
        from supriya.library import responselib
        arguments = (command,) + contents
        response = responselib.NodeInfoResponse(*arguments)
        return response

    def _handle_n_set(self, command, contents):
        from supriya.library import responselib
        node_id, remainder = contents[0], contents[1:]
        items = []
        for group in self._group_items(remainder, 2):
            item = responselib.NodeSetItem(*group)
            items.append(item)
        response = responselib.NodeSetResponse(
            node_id=node_id,
            items=tuple(items),
            )
        return response

    def _handle_n_setn(self, command, contents):
        from supriya.library import responselib
        node_id, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            control_index_or_name = remainder[0]
            control_count = remainder[1]
            control_values = tuple(remainder[2:2 + control_count])
            item = responselib.NodeSetContiguousItem(
                control_index_or_name=control_index_or_name,
                control_values=control_values,
                )
            items.append(item)
            remainder = remainder[2 + control_count:]
        items = tuple(items)
        response = responselib.NodeSetContiguousResponse(
            node_id=node_id,
            items=items,
            )
        return response

    def _handle_status_reply(self, command, contents):
        from supriya.library import responselib
        arguments = contents[1:]
        response = responselib.StatusResponse(*arguments)
        return response

    def _handle_synced(self, command, contents):
        from supriya.library import responselib
        arguments = contents
        response = responselib.SyncedResponse(*arguments)
        return response

    def _handle_tr(self, command, contents):
        from supriya.library import responselib
        arguments = contents
        response = responselib.TriggerResponse(*arguments)
        return response

    ### SPECIAL METHODS ###

    def __call__(self, message):
        address, contents = message.address, message.contents
        if address in self._response_handlers:
            handler = self._response_handlers[address]
            response = handler(address, contents)
        else:
            raise ValueError
        return response
