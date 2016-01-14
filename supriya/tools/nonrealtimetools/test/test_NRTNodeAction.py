# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nonrealtimetools
from supriya.tools import servertools


class TestCase(unittest.TestCase):

    def test_add_to_head_01(self):
        source = nonrealtimetools.NRTGroup(None, 1)
        target = nonrealtimetools.NRTGroup(None, 0)
        action = nonrealtimetools.NRTNodeAction(
            source=source,
            target=target,
            action=servertools.AddAction.ADD_TO_HEAD,
            )
        nodes_to_children = {
            target: None,
            }
        nodes_to_parent = {
            target: None,
            }
        action.apply_transform(nodes_to_children, nodes_to_parent)
        assert nodes_to_children == {
            source: None,
            target: (source,),
            }
        assert nodes_to_parent == {
            source: target,
            target: None,
            }
