# -*- encoding: utf-8 -*-
from supriya.tools import nonrealtimetools
from base import TestCase


class TestCase(TestCase):

    def test___graph___01(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            group_a = session.add_group(duration=20)
            group_a.add_synth(duration=20, amplitude=0.25)
            group_b = session.add_group(duration=20)
        with session.at(5):
            group_b.add_synth(duration=10)
        with session.at(10):
            group_c = session.add_group(duration=10)
        with session.at(15):
            group_a.move_node(group_c)
        graphviz_graph = session.__graph__()
        assert str(graphviz_graph) == self.normalize('''
            digraph G {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=TB,
                    ranksep=0.5,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=none,
                    style=rounded];
                edge [penwidth=2];
                subgraph cluster_0 {
                    graph [label="-inf"];
                    subgraph cluster_0_0 {
                    }
                    node_0_1 [label=<
                        <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">Root:0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                }
                subgraph cluster_1 {
                    graph [label="0"];
                    subgraph cluster_1_0 {
                        node_1_0_0 [label=<
                            <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                                <TR>
                                    <TD BORDER="0">S:1001<BR/>(da09821)</TD>
                                </TR>
                                <HR/>
                                <TR>
                                    <TD BORDER="0">0.0:20.0</TD>
                                </TR>
                            </TABLE>>,
                            margin=0.05];
                    }
                    node_1_1 [label=<
                        <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">Root:0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_1_2 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1002</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_1_3 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1000</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_1_1 -> node_1_2;
                    node_1_1 -> node_1_3;
                    node_1_3 -> node_1_0_0;
                }
                subgraph cluster_2 {
                    graph [label="5"];
                    subgraph cluster_2_0 {
                        node_2_0_0 [label=<
                            <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                                <TR>
                                    <TD BORDER="0">S:1003<BR/>(da09821)</TD>
                                </TR>
                                <HR/>
                                <TR>
                                    <TD BORDER="0">5.0:15.0</TD>
                                </TR>
                            </TABLE>>,
                            margin=0.05];
                        node_2_0_1 [label=<
                            <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                                <TR>
                                    <TD BORDER="0">S:1001<BR/>(da09821)</TD>
                                </TR>
                                <HR/>
                                <TR>
                                    <TD BORDER="0">0.0:20.0</TD>
                                </TR>
                            </TABLE>>,
                            margin=0.05];
                    }
                    node_2_1 [label=<
                        <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">Root:0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_2_2 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1002</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_2_3 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1000</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_2_1 -> node_2_2;
                    node_2_1 -> node_2_3;
                    node_2_2 -> node_2_0_0;
                    node_2_3 -> node_2_0_1;
                }
                subgraph cluster_3 {
                    graph [label="10"];
                    subgraph cluster_3_0 {
                        node_3_0_0 [label=<
                            <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                                <TR>
                                    <TD BORDER="0">S:1003<BR/>(da09821)</TD>
                                </TR>
                                <HR/>
                                <TR>
                                    <TD BORDER="0">5.0:15.0</TD>
                                </TR>
                            </TABLE>>,
                            margin=0.05];
                        node_3_0_1 [label=<
                            <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                                <TR>
                                    <TD BORDER="0">S:1001<BR/>(da09821)</TD>
                                </TR>
                                <HR/>
                                <TR>
                                    <TD BORDER="0">0.0:20.0</TD>
                                </TR>
                            </TABLE>>,
                            margin=0.05];
                    }
                    node_3_1 [label=<
                        <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">Root:0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_3_2 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1004</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">10.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_3_3 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1002</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_3_4 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1000</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_3_1 -> node_3_2;
                    node_3_1 -> node_3_3;
                    node_3_1 -> node_3_4;
                    node_3_3 -> node_3_0_0;
                    node_3_4 -> node_3_0_1;
                }
                subgraph cluster_4 {
                    graph [label="15.0"];
                    subgraph cluster_4_0 {
                        node_4_0_0 [label=<
                            <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                                <TR>
                                    <TD BORDER="0">S:1001<BR/>(da09821)</TD>
                                </TR>
                                <HR/>
                                <TR>
                                    <TD BORDER="0">0.0:20.0</TD>
                                </TR>
                            </TABLE>>,
                            margin=0.05];
                    }
                    node_4_1 [label=<
                        <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">Root:0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_4_2 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1002</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_4_3 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1000</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_4_4 [label=<
                        <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">G:1004</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">10.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_4_1 -> node_4_2;
                    node_4_1 -> node_4_3;
                    node_4_3 -> node_4_0_0;
                    node_4_3 -> node_4_4;
                }
                subgraph cluster_5 {
                    graph [label="20.0"];
                    subgraph cluster_5_0 {
                    }
                    node_5_1 [label=<
                        <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">Root:0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                }
            }
        ''')
