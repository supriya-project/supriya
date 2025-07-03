import pytest
from pytest_lazy_fixtures import lf
from uqbar.strings import normalize

from supriya import SynthDef, SynthDefBuilder, default
from supriya.ugens import FFT, MFCC, In, Out


@pytest.fixture
def mfcc_synthdef():
    with SynthDefBuilder() as builder:
        source = In.ar(bus=0)
        pv_chain = FFT.kr(source=source)
        mfcc = MFCC.kr(pv_chain=pv_chain)
        Out.kr(bus=0, source=mfcc)
    return builder.build("test:mfcc")


@pytest.mark.parametrize(
    "synthdef, expected_str",
    [
        (
            default,
            r"""
            digraph "synthdef_supriya:default" {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    ranksep=1,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=Mrecord,
                    style="filled, rounded"];
                edge [penwidth=2];
                ugen_0 [fillcolor=lightsalmon2,
                    label="<f_0> Control\n(scalar) | { { <f_1_0_0> out:\n0.0 } }"];
                ugen_1 [fillcolor=lightgoldenrod2,
                    label="<f_0> Control\n(control) | { { <f_1_0_0> amplitude:\n0.1 | <f_1_0_1> frequency:\n440.0 | <f_1_0_2> gate:\n1.0 | <f_1_0_3> pan:\n0.5 } }"];
                ugen_2 [fillcolor=lightsteelblue2,
                    label="<f_0> VarSaw\n(audio) | { { <f_1_0_0> frequency | <f_1_0_1> initial_phase:\n0.0 | <f_1_0_2> width:\n0.3 } | { <f_1_1_0> 0 } }"];
                ugen_3 [fillcolor=lightgoldenrod2,
                    label="<f_0> Linen\n(control) | { { <f_1_0_0> gate | <f_1_0_1> attack_time:\n0.01 | <f_1_0_2> sustain_level:\n0.7 | <f_1_0_3> release_time:\n0.3 | <f_1_0_4> done_action:\n2.0 } | { <f_1_1_0> 0 } }"];
                ugen_4 [fillcolor=lightsalmon2,
                    label="<f_0> Rand\n(scalar) | { { <f_1_0_0> minimum:\n-0.4 | <f_1_0_1> maximum:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_5 [fillcolor=lightgoldenrod2,
                    label="<f_0> BinaryOpUGen\n[ADDITION]\n(control) | { { <f_1_0_0> left | <f_1_0_1> right } | { <f_1_1_0> 0 } }"];
                ugen_6 [fillcolor=lightsteelblue2,
                    label="<f_0> VarSaw\n(audio) | { { <f_1_0_0> frequency | <f_1_0_1> initial_phase:\n0.0 | <f_1_0_2> width:\n0.3 } | { <f_1_1_0> 0 } }"];
                ugen_7 [fillcolor=lightsalmon2,
                    label="<f_0> Rand\n(scalar) | { { <f_1_0_0> minimum:\n0.0 | <f_1_0_1> maximum:\n0.4 } | { <f_1_1_0> 0 } }"];
                ugen_8 [fillcolor=lightgoldenrod2,
                    label="<f_0> BinaryOpUGen\n[ADDITION]\n(control) | { { <f_1_0_0> left | <f_1_0_1> right } | { <f_1_1_0> 0 } }"];
                ugen_9 [fillcolor=lightsteelblue2,
                    label="<f_0> VarSaw\n(audio) | { { <f_1_0_0> frequency | <f_1_0_1> initial_phase:\n0.0 | <f_1_0_2> width:\n0.3 } | { <f_1_1_0> 0 } }"];
                ugen_10 [fillcolor=lightsteelblue2,
                    label="<f_0> Sum3\n(audio) | { { <f_1_0_0> input_one | <f_1_0_1> input_two | <f_1_0_2> input_three } | { <f_1_1_0> 0 } }"];
                ugen_11 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[MULTIPLICATION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right:\n0.3 } | { <f_1_1_0> 0 } }"];
                ugen_12 [fillcolor=lightsalmon2,
                    label="<f_0> Rand\n(scalar) | { { <f_1_0_0> minimum:\n4000.0 | <f_1_0_1> maximum:\n5000.0 } | { <f_1_1_0> 0 } }"];
                ugen_13 [fillcolor=lightsalmon2,
                    label="<f_0> Rand\n(scalar) | { { <f_1_0_0> minimum:\n2500.0 | <f_1_0_1> maximum:\n3200.0 } | { <f_1_1_0> 0 } }"];
                ugen_14 [fillcolor=lightgoldenrod2,
                    label="<f_0> XLine\n(control) | { { <f_1_0_0> start | <f_1_0_1> stop | <f_1_0_2> duration:\n1.0 | <f_1_0_3> done_action:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_15 [fillcolor=lightsteelblue2,
                    label="<f_0> LPF\n(audio) | { { <f_1_0_0> source | <f_1_0_1> frequency } | { <f_1_1_0> 0 } }"];
                ugen_16 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[MULTIPLICATION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right } | { <f_1_1_0> 0 } }"];
                ugen_17 [fillcolor=lightsteelblue2,
                    label="<f_0> BinaryOpUGen\n[MULTIPLICATION]\n(audio) | { { <f_1_0_0> left | <f_1_0_1> right } | { <f_1_1_0> 0 } }"];
                ugen_18 [fillcolor=lightsteelblue2,
                    label="<f_0> Pan2\n(audio) | { { <f_1_0_0> source | <f_1_0_1> position | <f_1_0_2> level:\n1.0 } | { <f_1_1_0> 0 | <f_1_1_1> 1 } }"];
                ugen_19 [fillcolor=lightsteelblue2,
                    label="<f_0> OffsetOut\n(audio) | { { <f_1_0_0> bus | <f_1_0_1> source[0] | <f_1_0_2> source[1] } }"];
                ugen_0:f_1_0_0:e -> ugen_19:f_1_0_0:w [color=salmon];
                ugen_1:f_1_0_0:e -> ugen_17:f_1_0_1:w [color=goldenrod];
                ugen_1:f_1_0_1:e -> ugen_2:f_1_0_0:w [color=goldenrod];
                ugen_1:f_1_0_1:e -> ugen_5:f_1_0_0:w [color=goldenrod];
                ugen_1:f_1_0_1:e -> ugen_8:f_1_0_0:w [color=goldenrod];
                ugen_1:f_1_0_2:e -> ugen_3:f_1_0_0:w [color=goldenrod];
                ugen_1:f_1_0_3:e -> ugen_18:f_1_0_1:w [color=goldenrod];
                ugen_2:f_1_1_0:e -> ugen_10:f_1_0_0:w [color=steelblue];
                ugen_3:f_1_1_0:e -> ugen_16:f_1_0_1:w [color=goldenrod];
                ugen_4:f_1_1_0:e -> ugen_5:f_1_0_1:w [color=salmon];
                ugen_5:f_1_1_0:e -> ugen_6:f_1_0_0:w [color=goldenrod];
                ugen_6:f_1_1_0:e -> ugen_10:f_1_0_1:w [color=steelblue];
                ugen_7:f_1_1_0:e -> ugen_8:f_1_0_1:w [color=salmon];
                ugen_8:f_1_1_0:e -> ugen_9:f_1_0_0:w [color=goldenrod];
                ugen_9:f_1_1_0:e -> ugen_10:f_1_0_2:w [color=steelblue];
                ugen_10:f_1_1_0:e -> ugen_11:f_1_0_0:w [color=steelblue];
                ugen_11:f_1_1_0:e -> ugen_15:f_1_0_0:w [color=steelblue];
                ugen_12:f_1_1_0:e -> ugen_14:f_1_0_0:w [color=salmon];
                ugen_13:f_1_1_0:e -> ugen_14:f_1_0_1:w [color=salmon];
                ugen_14:f_1_1_0:e -> ugen_15:f_1_0_1:w [color=goldenrod];
                ugen_15:f_1_1_0:e -> ugen_16:f_1_0_0:w [color=steelblue];
                ugen_16:f_1_1_0:e -> ugen_17:f_1_0_0:w [color=steelblue];
                ugen_17:f_1_1_0:e -> ugen_18:f_1_0_0:w [color=steelblue];
                ugen_18:f_1_1_0:e -> ugen_19:f_1_0_1:w [color=steelblue];
                ugen_18:f_1_1_1:e -> ugen_19:f_1_0_2:w [color=steelblue];
            }
            """,
        ),
        (
            lf("mfcc_synthdef"),
            r"""
            digraph "synthdef_test:mfcc" {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    ranksep=1,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=Mrecord,
                    style="filled, rounded"];
                edge [penwidth=2];
                ugen_0 [fillcolor=lightsteelblue2,
                    label="<f_0> In\n(audio) | { { <f_1_0_0> bus:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_1 [fillcolor=lightsalmon2,
                    label="<f_0> MaxLocalBufs\n(scalar) | { { <f_1_0_0> maximum:\n1.0 } | { <f_1_1_0> 0 } }"];
                ugen_2 [fillcolor=lightsalmon2,
                    label="<f_0> LocalBuf\n(scalar) | { { <f_1_0_0> channel_count:\n1.0 | <f_1_0_1> frame_count:\n2048.0 } | { <f_1_1_0> 0 } }"];
                ugen_3 [fillcolor=lightgoldenrod2,
                    label="<f_0> FFT\n(control) | { { <f_1_0_0> buffer_id | <f_1_0_1> source | <f_1_0_2> hop:\n0.5 | <f_1_0_3> window_type:\n0.0 | <f_1_0_4> active:\n1.0 | <f_1_0_5> window_size:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_4 [fillcolor=lightgoldenrod2,
                    label="<f_0> MFCC\n(control) | { { <f_1_0_0> pv_chain | <f_1_0_1> coeff_count:\n13.0 } | { <f_1_1_0> 0 | <f_1_1_1> 1 | <f_1_1_2> 2 | <f_1_1_3> 3 | <f_1_1_4> 4 | <f_1_1_5> 5 | <f_1_1_6> 6 | <f_1_1_7> 7 | <f_1_1_8> 8 | <f_1_1_9> 9 | <f_1_1_10> 10 | <f_1_1_11> 11 | <f_1_1_12> 12 } }"];
                ugen_5 [fillcolor=lightgoldenrod2,
                    label="<f_0> Out\n(control) | { { <f_1_0_0> bus:\n0.0 | <f_1_0_1> source[0] | <f_1_0_2> source[1] | <f_1_0_3> source[2] | <f_1_0_4> source[3] | <f_1_0_5> source[4] | <f_1_0_6> source[5] | <f_1_0_7> source[6] | <f_1_0_8> source[7] | <f_1_0_9> source[8] | <f_1_0_10> source[9] | <f_1_0_11> source[10] | <f_1_0_12> source[11] | <f_1_0_13> source[12] } }"];
                ugen_0:f_1_1_0:e -> ugen_3:f_1_0_1:w [color=steelblue];
                ugen_2:f_1_1_0:e -> ugen_3:f_1_0_0:w [color=salmon];
                ugen_3:f_1_1_0:e -> ugen_4:f_1_0_0:w [color=goldenrod];
                ugen_4:f_1_1_0:e -> ugen_5:f_1_0_1:w [color=goldenrod];
                ugen_4:f_1_1_1:e -> ugen_5:f_1_0_2:w [color=goldenrod];
                ugen_4:f_1_1_2:e -> ugen_5:f_1_0_3:w [color=goldenrod];
                ugen_4:f_1_1_3:e -> ugen_5:f_1_0_4:w [color=goldenrod];
                ugen_4:f_1_1_4:e -> ugen_5:f_1_0_5:w [color=goldenrod];
                ugen_4:f_1_1_5:e -> ugen_5:f_1_0_6:w [color=goldenrod];
                ugen_4:f_1_1_6:e -> ugen_5:f_1_0_7:w [color=goldenrod];
                ugen_4:f_1_1_7:e -> ugen_5:f_1_0_8:w [color=goldenrod];
                ugen_4:f_1_1_8:e -> ugen_5:f_1_0_9:w [color=goldenrod];
                ugen_4:f_1_1_9:e -> ugen_5:f_1_0_10:w [color=goldenrod];
                ugen_4:f_1_1_10:e -> ugen_5:f_1_0_11:w [color=goldenrod];
                ugen_4:f_1_1_11:e -> ugen_5:f_1_0_12:w [color=goldenrod];
                ugen_4:f_1_1_12:e -> ugen_5:f_1_0_13:w [color=goldenrod];
            }
            """,
        ),
    ],
)
def test_SynthDef___graph__(synthdef: SynthDef, expected_str: str) -> None:
    graph = synthdef.__graph__()
    actual_str = format(graph, "graphviz")
    assert normalize(actual_str) == normalize(expected_str)
