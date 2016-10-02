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
            group_b.add_synth(duration=20)
            group_c = group_b.add_group(duration=20)
            group_c.add_synth(duration=20, frequency=330)
            session.add_synth(duration=20, frequency=880, out=8)
            group_b['pan'] = 0.25
            group_c['pan'] = 0.75
        graphviz_graph = session.states[0].__graph__(include_controls=False)
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
                    node_0_0 [label=<
                        <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">S:1006<BR/>(da09821)</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_0_1 [label=<
                        <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">S:1005<BR/>(da09821)</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_0_2 [label=<
                        <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">S:1003<BR/>(da09821)</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_0_3 [label=<
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
                node_1 [label=<
                    <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                        <TR>
                            <TD BORDER="0">Root:0</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05];
                node_2 [label=<
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
                node_3 [label=<
                    <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                        <TR>
                            <TD BORDER="0">G:1004</TD>
                        </TR>
                        <HR/>
                        <TR>
                            <TD BORDER="0">0.0:20.0</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05];
                node_4 [label=<
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
                node_1 -> node_0_0;
                node_1 -> node_2;
                node_1 -> node_4;
                node_2 -> node_0_2;
                node_2 -> node_3;
                node_3 -> node_0_1;
                node_4 -> node_0_3;
            }
        ''')
        graphviz_graph = session.states[0].__graph__(include_controls=True)
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
                    node_0_0 [label=<
                        <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">S:1006<BR/>(da09821)</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">amplitude: 0.1</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BGCOLOR="STEELBLUE2" BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">frequency: 880.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">gate: 1.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BGCOLOR="STEELBLUE2" BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">out: 8.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">pan: 0.5</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_0_1 [label=<
                        <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">S:1005<BR/>(da09821)</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">amplitude: 0.1</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BGCOLOR="STEELBLUE2" BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">frequency: 330.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">gate: 1.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">out: 0.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">pan: 0.5</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_0_2 [label=<
                        <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">S:1003<BR/>(da09821)</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">amplitude: 0.1</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">frequency: 440.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">gate: 1.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">out: 0.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">pan: 0.5</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                    node_0_3 [label=<
                        <TABLE BGCOLOR="LIGHTSTEELBLUE2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                            <TR>
                                <TD BORDER="0">S:1001<BR/>(da09821)</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BGCOLOR="STEELBLUE2" BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">amplitude: 0.25</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">frequency: 440.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">gate: 1.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">out: 0.0</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">pan: 0.5</FONT></TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">0.0:20.0</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05];
                }
                node_1 [label=<
                    <TABLE BGCOLOR="LIGHTSALMON2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                        <TR>
                            <TD BORDER="0">Root:0</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05];
                node_2 [label=<
                    <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                        <TR>
                            <TD BORDER="0">G:1002</TD>
                        </TR>
                        <HR/>
                        <TR>
                            <TD BGCOLOR="GOLDENROD2" BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">pan: 0.25</FONT></TD>
                        </TR>
                        <HR/>
                        <TR>
                            <TD BORDER="0">0.0:20.0</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05];
                node_3 [label=<
                    <TABLE BGCOLOR="LIGHTGOLDENROD2" BORDER="2" CELLBORDER="0" CELLPADDING="5" CELLSPACING="0" STYLE="ROUNDED">
                        <TR>
                            <TD BORDER="0">G:1004</TD>
                        </TR>
                        <HR/>
                        <TR>
                            <TD BGCOLOR="GOLDENROD2" BORDER="0" CELLPADDING="2"><FONT POINT-SIZE="8">pan: 0.75</FONT></TD>
                        </TR>
                        <HR/>
                        <TR>
                            <TD BORDER="0">0.0:20.0</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05];
                node_4 [label=<
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
                node_1 -> node_0_0;
                node_1 -> node_2;
                node_1 -> node_4;
                node_2 -> node_0_2;
                node_2 -> node_3;
                node_3 -> node_0_1;
                node_4 -> node_0_3;
            }
        ''')
