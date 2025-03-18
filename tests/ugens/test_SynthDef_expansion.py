import os
import platform

import pytest
from uqbar.strings import normalize

from supriya.ugens import SuperColliderSynthDef, decompile_synthdef


@pytest.fixture
def sc_synthdef_expansion() -> SuperColliderSynthDef:
    return SuperColliderSynthDef(
        "expansionTest",
        """
        var a, b, c, d;
        a = SinOsc.ar([1, 2]);
        b = Pan2.ar(a);
        c = Pan2.ar(b).softclip;
        Out.ar(0, c);
        """,
    )


@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_sc_format(sc_synthdef_expansion: SuperColliderSynthDef) -> None:
    sc_compiled_synthdef = bytes(sc_synthdef_expansion.compile())
    sc_synthdef = decompile_synthdef(sc_compiled_synthdef)
    assert str(sc_synthdef) == normalize(
        """
        synthdef:
            name: expansionTest
            ugens:
            -   SinOsc.ar/0:
                    frequency: 1.0
                    phase: 0.0
            -   Pan2.ar/0:
                    source: SinOsc.ar/0[0]
                    position: 0.0
                    level: 1.0
            -   Pan2.ar/1:
                    source: Pan2.ar/0[0]
                    position: 0.0
                    level: 1.0
            -   UnaryOpUGen(SOFTCLIP).ar/0:
                    source: Pan2.ar/1[0]
            -   UnaryOpUGen(SOFTCLIP).ar/1:
                    source: Pan2.ar/1[1]
            -   Pan2.ar/2:
                    source: Pan2.ar/0[1]
                    position: 0.0
                    level: 1.0
            -   UnaryOpUGen(SOFTCLIP).ar/2:
                    source: Pan2.ar/2[0]
            -   UnaryOpUGen(SOFTCLIP).ar/3:
                    source: Pan2.ar/2[1]
            -   SinOsc.ar/1:
                    frequency: 2.0
                    phase: 0.0
            -   Pan2.ar/3:
                    source: SinOsc.ar/1[0]
                    position: 0.0
                    level: 1.0
            -   Pan2.ar/4:
                    source: Pan2.ar/3[0]
                    position: 0.0
                    level: 1.0
            -   UnaryOpUGen(SOFTCLIP).ar/4:
                    source: Pan2.ar/4[0]
            -   Out.ar/0:
                    bus: 0.0
                    source[0]: UnaryOpUGen(SOFTCLIP).ar/0[0]
                    source[1]: UnaryOpUGen(SOFTCLIP).ar/4[0]
            -   UnaryOpUGen(SOFTCLIP).ar/5:
                    source: Pan2.ar/4[1]
            -   Out.ar/1:
                    bus: 0.0
                    source[0]: UnaryOpUGen(SOFTCLIP).ar/1[0]
                    source[1]: UnaryOpUGen(SOFTCLIP).ar/5[0]
            -   Pan2.ar/5:
                    source: Pan2.ar/3[1]
                    position: 0.0
                    level: 1.0
            -   UnaryOpUGen(SOFTCLIP).ar/6:
                    source: Pan2.ar/5[0]
            -   Out.ar/2:
                    bus: 0.0
                    source[0]: UnaryOpUGen(SOFTCLIP).ar/2[0]
                    source[1]: UnaryOpUGen(SOFTCLIP).ar/6[0]
            -   UnaryOpUGen(SOFTCLIP).ar/7:
                    source: Pan2.ar/5[1]
            -   Out.ar/3:
                    bus: 0.0
                    source[0]: UnaryOpUGen(SOFTCLIP).ar/3[0]
                    source[1]: UnaryOpUGen(SOFTCLIP).ar/7[0]
        """
    )
