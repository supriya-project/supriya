# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class TimespanCollectionNode(SupriyaObject):
    r'''A node in a timespan collection.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_balance',
        '_height',
        '_left_child',
        '_node_start_index',
        '_node_stop_index',
        '_payload',
        '_right_child',
        '_start_offset',
        '_stop_offset_high',
        '_stop_offset_low',
        '_subtree_start_index',
        '_subtree_stop_index',
        )

    ### INITIALIZER ###

    def __init__(self, start_offset):
        self._balance = 0
        self._height = 0
        self._left_child = None
        self._node_start_index = -1
        self._node_stop_index = -1
        self._payload = []
        self._right_child = None
        self._start_offset = start_offset
        self._stop_offset_high = None
        self._stop_offset_low = None
        self._subtree_start_index = -1
        self._subtree_stop_index = -1

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets the repr of this timespan collection node.
        '''
        return '<Node: Start:{} Indices:({}:{}:{}:{}) Length:{{{}}}>'.format(
            self.start_offset,
            self.subtree_start_index,
            self.node_start_index,
            self.node_stop_index,
            self.subtree_stop_index,
            len(self.payload),
            )

    ### PRIVATE METHODS ###

    def _debug(self):
        return '\n'.join(self._get_debug_pieces())

    def _get_debug_pieces(self):
        result = []
        result.append(repr(self))
        if self.left_child:
            subresult = self.left_child._get_debug_pieces()
            result.append('\tL: {}'.format(subresult[0]))
            result.extend('\t' + x for x in subresult[1:])
        if self.right_child:
            subresult = self.right_child._get_debug_pieces()
            result.append('\tR: {}'.format(subresult[0]))
            result.extend('\t' + x for x in subresult[1:])
        return result

    def _update(self):
        left_height = -1
        right_height = -1
        if self.left_child is not None:
            left_height = self.left_child.height
        if self.right_child is not None:
            right_height = self.right_child.height
        self._height = max(left_height, right_height) + 1
        self._balance = right_height - left_height
        return self.height

    ### PUBLIC PROPERTIES ###

    @property
    def balance(self):
        r'''Gets the balance of this timespan collection node.
        '''
        return self._balance

    @property
    def height(self):
        r'''Gets the height of this timespan collection node.
        '''
        return self._height

    @property
    def left_child(self):
        r'''Gets and sets the left child of this timespan collection node.
        '''
        return self._left_child

    @left_child.setter
    def left_child(self, node):
        self._left_child = node
        self._update()

    @property
    def node_start_index(self):
        r'''Gets the node start index of this timespan collection node.
        '''
        return self._node_start_index

    @property
    def node_stop_index(self):
        r'''Gets the node stop index of this timespan collection node.
        '''
        return self._node_stop_index

    @property
    def payload(self):
        r'''Gets the payload of this timespan collection node.
        '''
        return self._payload

    @property
    def right_child(self):
        r'''Gets and sets the right child of this timespan collection node.
        '''
        return self._right_child

    @right_child.setter
    def right_child(self, node):
        self._right_child = node
        self._update()

    @property
    def start_offset(self):
        r'''Gets the start offset of this timespan collection node.
        '''
        return self._start_offset

    @property
    def stop_offset_high(self):
        r'''Gets the highest stop offset of the subtree rooted on this timespan
        collection node.
        '''
        return self._stop_offset_high

    @property
    def stop_offset_low(self):
        r'''Gets the lowest stop offset of the subtree rooted on this timespan
        collection node.
        '''
        return self._stop_offset_low

    @property
    def subtree_start_index(self):
        r'''Gets the start index of the subtree rooted on this timespan
        collection node.
        '''
        return self._subtree_start_index

    @property
    def subtree_stop_index(self):
        r'''Gets the stop index of the subtree rooted on this timespan
        collection node.
        '''
        return self._subtree_stop_index
