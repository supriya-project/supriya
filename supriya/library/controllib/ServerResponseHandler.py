# -*- encoding: utf-8 -*-
import collections
import itertools
import sys


class ServerResponseHandler(object):
    r'''Handles OSC responses from scsynth.

    ::

        >>> from supriya import controllib
        >>> from supriya import osclib
        >>> handler = controllib.ServerResponseHandler()

    ::

        >>> message = osclib.OscMessage(
        ...     '/status.reply', 1, 0, 0, 2, 4,
        ...     0.040679048746824265, 0.15118031203746796,
        ...     44100.0, 44100.00077873274,
        ...     )
        >>> handler(message)
        StatusReplyResponse(
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
        >>> handler(message)
        BInfoResponse(
            buffer_id=1100,
            frame_count=512,
            channel_count=1,
            sample_rate=44100.0
            )

    ::

        >>> message = osclib.OscMessage('/n_set', 1023, '/one', -1, '/two', 0)
        >>> handler(message)
        NSetResponse(node_id=1023, items=(NSetItem(control_index_or_name='/one', control_value=-1), NSetItem(control_index_or_name='/two', control_value=0)))

    ::

        >>> message = osclib.OscMessage('/b_setn', 1, 0, 8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        >>> handler(message)
        BSetnResponse(buffer_number=1, items=(BSetnItem(starting_sample_index=0, sample_values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)),))

    '''

    ### CLASS VARIABLES ###

    BSetItem = collections.namedtuple(
        'BSetItem',
        (
            'sample_index',
            'sample_value',
            ),
        )

    BSetResponse = collections.namedtuple(
        'BSetResponse',
        (
            'buffer_number',
            'items',
            ),
        )

    BSetnItem = collections.namedtuple(
        'BSetnItem',
        (
            'starting_sample_index',
            'sample_values',
            ),
        )

    BSetnResponse = collections.namedtuple(
        'BSetnResponse',
        (
            'buffer_number',
            'items',
            ),
        )

    CSetItem = collections.namedtuple(
        'CSetItem',
        (
            'bus_index',
            'bus_value',
            ),
        )

    CSetResponse = collections.namedtuple(
        'CSetResponse',
        (
            'items',
            ),
        )

    CSetnItem = collections.namedtuple(
        'CSetnItem',
        (
            'starting_bus_index',
            'bus_values',
            ),
        )

    CSetnResponse = collections.namedtuple(
        'CSetnResponse',
        (
            'items',
            ),
        )

    DoneResponse = collections.namedtuple(
        'DoneResponse',
        (
            'action',
            ),
        )

    FailResponse = collections.namedtuple(
        'FailResponse',
        (
            'failed_command',
            'failure_reason',
            ),
        )

    GQueryTreeControlItem = collections.namedtuple(
        'GQueryTreeControlItem',
        (
            'control_name_or_index',
            'control_value',
            ),
        )

    GQueryTreeGroupItem = collections.namedtuple(
        'GQueryTreeSynthItem',
        (
            'node_id',
            'child_count',
            ),
        )

    GQueryTreeSynthItem = collections.namedtuple(
        'GQueryTreeSynthItem',
        (
            'node_id',
            'synth_definition_name',
            'controls',
            ),
        )

    GQueryTreeResponse = collections.namedtuple(
        'GQueryTreeResponse',
        (
            'node_id',
            'child_count',
            'items',
            ),
        )

    NSetItem = collections.namedtuple(
        'NSetItem',
        (
            'control_index_or_name',
            'control_value',
            ),
        )

    NSetResponse = collections.namedtuple(
        'NSetResponse',
        (
            'node_id',
            'items',
            ),
        )

    NSetnItem = collections.namedtuple(
        'NSetnItem',
        (
            'starting_control_index_or_name',
            'control_values',
            ),
        )

    NSetnResponse = collections.namedtuple(
        'NSetnResponse',
        (
            'node_id'
            'items',
            ),
        )

    SyncedResponse = collections.namedtuple(
        'SyncedResponse',
        (
            'sync_id',
            ),
        )

    ### INITIALIZER ###

    def __init__(self):
        self._response_handlers = {
            '/b_info': self._handle_b_info,
            '/b_set': self._handle_b_set,
            '/b_setn': self._handle_b_setn,
            '/c_set': self._handle_c_set,
            '/c_setn': self._handle_c_setn,
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
        from supriya.library import controllib
        arguments = contents
        response = controllib.BInfoResponse(*arguments)
        return response

    def _handle_b_set(self, command, contents):
        buffer_number, remainder = contents[0], contents[1:]
        items = []
        for group in self._group_items(remainder, 2):
            item = self.BSetItem(*group)
            items.append(item)
        items = tuple(items)
        response = self.BSetResponse(
            buffer_number=buffer_number,
            items=items,
            )
        return response

    def _handle_b_setn(self, command, contents):
        buffer_number, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            starting_sample_index = remainder[0]
            sample_count = remainder[1]
            sample_values = tuple(remainder[2:2 + sample_count])
            item = self.BSetnItem(
                starting_sample_index=starting_sample_index,
                sample_values=sample_values,
                )
            items.append(item)
            remainder = remainder[2 + sample_count:]
        items = tuple(items)
        response = self.BSetnResponse(
            buffer_number=buffer_number,
            items=items,
            )
        return response

    def _handle_c_set(self, command, contents):
        items = []
        for group in self._group_items(contents, 2):
            item = self.CSetItem(*group)
            items.append(item)
        response = self.CSetResponse(
            items=tuple(items),
            )
        return response

    def _handle_c_setn(self, command, contents):
        items = []
        while contents:
            starting_bus_index = contents[0]
            bus_count = contents[1]
            bus_values = tuple(contents[2:2 + bus_count])
            item = self.CSetnItem(
                starting_bus_index=starting_bus_index,
                bus_values=bus_values,
                )
            items.append(item)
            contents = contents[2 + bus_count:]
        items = tuple(items)
        response = self.CSetnResponse(
            items=items,
            )
        return response

    def _handle_fail(self, command, contents):
        arguments = contents
        response = self.FailResponse(*arguments)
        return response

    def _handle_g_query_tree_reply(self, command, contents):
        raise NotImplementedError('Not yet implemented.')

    def _handle_n_info(self, command, contents):
        from supriya.library import controllib
        arguments = (command,) + contents
        response = controllib.NodeResponse(*arguments)
        return response

    def _handle_n_set(self, command, contents):
        node_id, remainder = contents[0], contents[1:]
        items = []
        for group in self._group_items(remainder, 2):
            item = self.NSetItem(*group)
            items.append(item)
        response = self.NSetResponse(
            node_id=node_id,
            items=tuple(items),
            )
        return response

    def _handle_n_setn(self, command, contents):
        node_id, remainder = contents[0], contents[1:]
        items = []
        while remainder:
            control_index_or_name = remainder[0]
            control_count = remainder[1]
            control_values = tuple(remainder[2:2 + control_count])
            item = self.NSetnItem(
                control_index_or_name=control_index_or_name,
                control_values=control_values,
                )
            items.append(item)
            remainder = remainder[2 + control_count:]
        items = tuple(items)
        response = self.NSetnResponse(
            node_id=node_id,
            items=items,
            )
        return response

    def _handle_status_reply(self, command, contents):
        from supriya.library import controllib
        arguments = contents[1:]
        response = controllib.StatusReplyResponse(*arguments)
        return response

    def _handle_synced(self, command, contents):
        arguments = contents
        response = self.SyncedResponse(*arguments)
        return response

    def _handle_tr(self, command, contents):
        from supriya.library import controllib
        arguments = contents
        response = controllib.TrResponse(*arguments)
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
