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

        >>> message = osclib.OscMessage('/b_info', 1100, 512, 1, 44100.0)
        >>> handler(message)
        BInfoResponse(buffer_id=1100, frame_count=512, channel_count=1, sample_rate=44100.0)

    ::

        >>> message = osclib.OscMessage('/n_set', 1023, '/one', -1, '/two', 0)
        >>> handler(message)
        NSetResponse(node_id=1023, items=(NSetItem(control_index_or_name='/one', control_value=-1), NSetItem(control_index_or_name='/two', control_value=0)))

    '''

    ### CLASS VARIABLES ###

    BInfoResponse = collections.namedtuple(
        'BInfoResponse',
        (
            'buffer_id',
            'frame_count',
            'channel_count',
            'sample_rate',
            ),
        )

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

    NodeResponse = collections.namedtuple(
        'NodeResponse',
        (
            'message_head',
            'node_id',
            'parent_group_id',
            'previous_node_id',
            'next_node_id',
            'is_group',
            'head_node_id',
            'tail_node_id',
            ),
        )

    StatusReplyResponse = collections.namedtuple(
        'StatusReplyResponse',
        (
            'unused_int',
            'ugen_count',
            'synth_count',
            'group_count',
            'synth_definition_count',
            'average_cpu_usage',
            'peak_cpu_usage',
            'target_sample_rate',
            'actual_sample_rate',
            ),
        )

    SyncedResponse = collections.namedtuple(
        'SyncedResponse',
        (
            'sync_id',
            ),
        )

    TrResponse = collections.namedtuple(
        'TrResponse',
        (
            'node_id',
            'trigger_id',
            'trigger_value',
            ),
        )

    ### INITIALIZER ###

    def __init__(self):
        self._basic_response_templates = {
            '/b_info': (self.BInfoResponse, False),
            '/fail': (self.FailResponse, False),
            '/n_end': (self.NodeResponse, True),
            '/n_go': (self.NodeResponse, True),
            '/n_info': (self.NodeResponse, True),
            '/n_move': (self.NodeResponse, True),
            '/n_off': (self.NodeResponse, True),
            '/n_on': (self.NodeResponse, True),
            '/status.reply': (self.StatusReplyResponse, False),
            '/synced': (self.SyncedResponse, False),
            '/tr': (self.TrResponse, False),
            }
        self._compound_response_handlers = {
            '/b_set': self._handle_b_set,
            '/b_setn': self._handle_b_setn,
            '/c_set': self._handle_c_set,
            '/c_setn': self._handle_c_setn,
            '/n_set': self._handle_n_set,
            '/n_setn': self._handle_n_setn,
            '/g_queryTree.reply': self._handle_g_query_tree_reply,
            }

    ### PRIVATE METHODS ###

    def _group_items(self, items, length):
        iterators = [iter(items)] * length
        if sys.version_info[0] == 2:
            iterator = itertools.izip(*iterators)
        else:
            iterator = zip(*iterators)
        return iterator

    def _handle_b_set(self, contents):
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

    def _handle_b_setn(self, contents):
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

    def _handle_c_set(self, contents):
        items = []
        for group in self._group_items(contents, 2):
            item = self.CSetItem(*group)
            items.append(item)
        response = self.CSetResponse(
            items=tuple(items),
            )
        return response

    def _handle_c_setn(self, contents):
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

    def _handle_g_query_tree_reply(self, contents):
        raise NotImplementedError('Not yet implemented.')

    def _handle_n_set(self, contents):
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

    def _handle_n_setn(self, contents):
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

    ### SPECIAL METHODS ###

    def __call__(self, message):
        address, contents = message.address, message.contents
        if address in self._basic_response_templates:
            template, keep_message_head = \
                self._basic_response_templates[address]
            if keep_message_head:
                arguments = (address,) + contents
            else:
                arguments = contents
            response = template(*arguments)
        elif address in self._compound_response_handlers:
            handler = self._compound_response_handlers[address]
            response = handler(contents)
        else:
            raise ValueError

        return response
