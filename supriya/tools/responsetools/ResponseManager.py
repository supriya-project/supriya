# -*- encoding: utf-8 -*-
import itertools
import sys
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ResponseManager(SupriyaObject):
    r'''Handles OSC responses from scsynth.

    ::

        >>> from supriya import osctools
        >>> from supriya import responsetools
        >>> manager = responsetools.ResponseManager

    ::

        >>> message = osctools.OscMessage(
        ...     '/status.reply', 1, 0, 0, 2, 4,
        ...     0.040679048746824265, 0.15118031203746796,
        ...     44100.0, 44100.00077873274,
        ...     )
        >>> manager.handle_message(message)
        StatusResponse(
            ugen_count=0,
            synth_count=0,
            group_count=2,
            synthdef_count=4,
            average_cpu_usage=0.040679048746824265,
            peak_cpu_usage=0.15118031203746796,
            target_sample_rate=44100.0,
            actual_sample_rate=44100.00077873274
            )

    ::

        >>> message = osctools.OscMessage('/b_info', 1100, 512, 1, 44100.0)
        >>> manager.handle_message(message)[0]
        BufferInfoResponse(
            buffer_id=1100,
            frame_count=512,
            channel_count=1,
            sample_rate=44100.0
            )

    ::

        >>> message = osctools.OscMessage('/n_set', 1023, '/one', -1, '/two', 0)
        >>> manager.handle_message(message)
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

        >>> message = osctools.OscMessage('/b_setn', 1, 0, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        >>> manager.handle_message(message)
        BufferSetContiguousResponse(
            items=(
                BufferSetContiguousItem(
                    starting_sample_index=0,
                    sample_values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                    ),
                ),
            buffer_id=1
            )

    ::

        >>> message = osctools.OscMessage('/g_queryTree.reply', 0, 0, 1, 1, 2, 1001, 0, 1000, 1, 1002, 0)
        >>> manager.handle_message(message)
        QueryTreeResponse(
            query_tree_group=QueryTreeGroup(
                node_id=0,
                children=(
                    QueryTreeGroup(
                        node_id=1,
                        children=(
                            QueryTreeGroup(
                                node_id=1001,
                                children=()
                                ),
                            QueryTreeGroup(
                                node_id=1000,
                                children=(
                                    QueryTreeGroup(
                                        node_id=1002,
                                        children=()
                                        ),
                                    )
                                ),
                            )
                        ),
                    )
                )
            )

    ::

        >>> print(manager.handle_message(message))
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 group

    '''

    ### PUBLIC METHODS ###

    @staticmethod
    def group_items(items, length):
        iterators = [iter(items)] * length
        if sys.version_info[0] == 2:
            iterator = itertools.izip(*iterators)
        else:
            iterator = zip(*iterators)
        return iterator

    @staticmethod
    def handle_message(message):
        address, contents = message.address, message.contents
        if address in _response_handlers:
            handler = _response_handlers[address]
            response = handler(address, contents)
        else:
            raise ValueError(message)
        return response

    @staticmethod
    def handle_b_info(command, contents):
        from supriya.tools import responsetools
        responses = []
        for group in ResponseManager.group_items(contents, 4):
            response = responsetools.BufferInfoResponse(*group)
            responses.append(response)
        responses = tuple(responses)
        return responses

    @staticmethod
    def handle_b_set(command, contents):
        from supriya.tools import responsetools
        buffer_id, remainder = contents[0], contents[1:]
        items = []
        for group in ResponseManager.group_items(remainder, 2):
            item = responsetools.BufferSetItem(*group)
            items.append(item)
        items = tuple(items)
        response = responsetools.BufferSetResponse(
            buffer_id=buffer_id,
            items=items,
            )
        return response

    @staticmethod
    def handle_b_setn(command, contents):
        from supriya.tools import responsetools
        buffer_id, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            starting_sample_index = remainder[0]
            sample_count = remainder[1]
            sample_values = tuple(remainder[2:2 + sample_count])
            item = responsetools.BufferSetContiguousItem(
                starting_sample_index=starting_sample_index,
                sample_values=sample_values,
                )
            items.append(item)
            remainder = remainder[2 + sample_count:]
        items = tuple(items)
        response = responsetools.BufferSetContiguousResponse(
            buffer_id=buffer_id,
            items=items,
            )
        return response

    @staticmethod
    def handle_c_set(command, contents):
        from supriya.tools import responsetools
        items = []
        for group in ResponseManager.group_items(contents, 2):
            item = responsetools.ControlBusSetItem(*group)
            items.append(item)
        response = responsetools.ControlBusSetResponse(
            items=tuple(items),
            )
        return response

    @staticmethod
    def handle_c_setn(command, contents):
        from supriya.tools import responsetools
        items = []
        while contents:
            starting_bus_id = contents[0]
            bus_count = contents[1]
            bus_values = tuple(contents[2:2 + bus_count])
            item = responsetools.ControlBusSetContiguousItem(
                starting_bus_id=starting_bus_id,
                bus_values=bus_values,
                )
            items.append(item)
            contents = contents[2 + bus_count:]
        items = tuple(items)
        response = responsetools.CSetnResponse(
            items=items,
            )
        return response

    @staticmethod
    def handle_d_removed(command, contents):
        from supriya.tools import responsetools
        synthdef_name = contents[0]
        response = responsetools.SynthDefRemovedResponse(
            synthdef_name=synthdef_name,
            )
        return response

    @staticmethod
    def handle_done(command, contents):
        from supriya.tools import responsetools
        arguments = contents
        response = responsetools.DoneResponse(action=tuple(arguments))
        return response

    @staticmethod
    def handle_fail(command, contents):
        from supriya.tools import responsetools
        failed_command = contents[0]
        failure_reason = contents[1:]
        if failure_reason:
            failure_reason = tuple(failure_reason)
        response = responsetools.FailResponse(
            failed_command=failed_command,
            failure_reason=failure_reason,
            )
        return response

    @staticmethod
    def handle_g_query_tree_reply(command, contents):
        def recurse(contents, control_flag):
            node_id = contents.pop(0)
            child_count = contents.pop(0)
            if child_count == -1:
                controls = []
                synthdef_name = contents.pop(0)
                if control_flag:
                    control_count = contents.pop(0)
                    for i in range(control_count):
                        control_name_or_index = contents.pop(0)
                        control_value = contents.pop(0)
                        control = responsetools.QueryTreeControl(
                            control_name_or_index=control_name_or_index,
                            control_value=control_value,
                            )
                        controls.append(control)
                controls = tuple(controls)
                result = responsetools.QueryTreeSynth(
                    node_id=node_id,
                    synthdef_name=synthdef_name,
                    controls=controls,
                    )
            else:
                children = []
                for i in range(child_count):
                    children.append(recurse(contents, control_flag))
                children = tuple(children)
                result = responsetools.QueryTreeGroup(
                    node_id=node_id,
                    children=children,
                    )
            return result
        from supriya.tools import responsetools
        contents = list(contents)
        control_flag = bool(contents.pop(0))
        query_tree_group = recurse(contents, control_flag)
        response = responsetools.QueryTreeResponse(
            query_tree_group=query_tree_group,
            )
        return response

    @staticmethod
    def handle_n_info(command, contents):
        from supriya.tools import responsetools
        arguments = (command,) + contents
        response = responsetools.NodeInfoResponse(*arguments)
        return response

    @staticmethod
    def handle_n_set(command, contents):
        from supriya.tools import responsetools
        node_id, remainder = contents[0], contents[1:]
        items = []
        for group in ResponseManager.group_items(remainder, 2):
            item = responsetools.NodeSetItem(*group)
            items.append(item)
        response = responsetools.NodeSetResponse(
            node_id=node_id,
            items=tuple(items),
            )
        return response

    @staticmethod
    def handle_n_setn(command, contents):
        from supriya.tools import responsetools
        node_id, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            control_index_or_name = remainder[0]
            control_count = remainder[1]
            control_values = tuple(remainder[2:2 + control_count])
            item = responsetools.NodeSetContiguousItem(
                control_index_or_name=control_index_or_name,
                control_values=control_values,
                )
            items.append(item)
            remainder = remainder[2 + control_count:]
        items = tuple(items)
        response = responsetools.NodeSetContiguousResponse(
            node_id=node_id,
            items=items,
            )
        return response

    @staticmethod
    def handle_status_reply(command, contents):
        from supriya.tools import responsetools
        arguments = contents[1:]
        response = responsetools.StatusResponse(*arguments)
        return response

    @staticmethod
    def handle_synced(command, contents):
        from supriya.tools import responsetools
        arguments = contents
        response = responsetools.SyncedResponse(*arguments)
        return response

    @staticmethod
    def handle_tr(command, contents):
        from supriya.tools import responsetools
        arguments = contents
        response = responsetools.TriggerResponse(*arguments)
        return response


_response_handlers = {
    '/b_info': ResponseManager.handle_b_info,
    '/b_set': ResponseManager.handle_b_set,
    '/b_setn': ResponseManager.handle_b_setn,
    '/c_set': ResponseManager.handle_c_set,
    '/c_setn': ResponseManager.handle_c_setn,
    '/d_removed': ResponseManager.handle_d_removed,
    '/done': ResponseManager.handle_done,
    '/fail': ResponseManager.handle_fail,
    '/g_queryTree.reply': ResponseManager.handle_g_query_tree_reply,
    '/n_end': ResponseManager.handle_n_info,
    '/n_go': ResponseManager.handle_n_info,
    '/n_info': ResponseManager.handle_n_info,
    '/n_move': ResponseManager.handle_n_info,
    '/n_off': ResponseManager.handle_n_info,
    '/n_on': ResponseManager.handle_n_info,
    '/n_set': ResponseManager.handle_n_set,
    '/n_setn': ResponseManager.handle_n_setn,
    '/status.reply': ResponseManager.handle_status_reply,
    '/synced': ResponseManager.handle_synced,
    '/tr': ResponseManager.handle_tr,
    }