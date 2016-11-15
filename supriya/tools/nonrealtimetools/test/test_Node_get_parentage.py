# -*- encoding: utf-8 -*-
from nonrealtimetools_testbase import TestCase
from supriya.tools import nonrealtimetools


class TestCase(TestCase):

    def test_01(self):
        """
        With Session.at(...) context manager.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        with session.at(5):
            parentage = node.get_parentage()
        assert parentage == [node, group_one, session.root_node]
        with session.at(15):
            parentage = node.get_parentage()
        assert parentage == [node, group_two, session.root_node]

    def test_02(self):
        """
        With offset=... keyword.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        parentage = node.get_parentage(offset=5)
        assert parentage == [node, group_one, session.root_node]
        parentage = node.get_parentage(offset=15)
        assert parentage == [node, group_two, session.root_node]

    def test_03(self):
        """
        Without Session.at(...) context manager or offset keyword.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        with self.assertRaises(ValueError):
            node.get_parentage()

    def test_04(self):
        """
        With both Session.at(...) context manager and offset keyword.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        with session.at(5):
            parentage = node.get_parentage(offset=15)
        assert parentage == [node, group_two, session.root_node]
