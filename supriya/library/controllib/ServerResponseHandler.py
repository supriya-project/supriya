# -*- encoding: utf-8 -*-
import collections


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

    '''

    ### CLASS VARIABLES ###

    BInfoResponse = collections.namedtuple(
        'BInfoResponse',
        (
            'buffer_id',
            'frame_count',
            'channel_count',
            'sample_rate',
            )
        )

    FailResponse = collections.namedtuple(
        'FailResponse',
        (
            'failed_command',
            'failure_reason',
            )
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
            )
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
            )
        )

    SyncedResponse = collections.namedtuple(
        'SyncedResponse',
        (
            'sync_id',
            )
        )

    TrResponse = collections.namedtuple(
        'TrResponse',
        (
            'node_id',
            'trigger_id',
            'trigger_value',
            )
        )

    DoneResponse = collections.namedtuple(
        'DoneResponse',
        (
            'action',
            )
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

    def _handle_b_set(self, contents):
        pass

    def _handle_b_setn(self, contents):
        pass

    def _handle_c_set(self, contents):
        pass

    def _handle_c_setn(self, contents):
        pass

    def _handle_g_query_tree_reply(self, contents):
        pass

    def _handle_n_set(self, contents):
        pass

    def _handle_n_setn(self, contents):
        pass

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
        elif address in self.compound_response_handlers:
            handler = self.compound_response_handlers[address]
            response = handler(contents)
        else:
            raise ValueError

        return response
